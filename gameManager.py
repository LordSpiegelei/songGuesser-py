import time
from threading import Thread
import re

import serverCore
import menuManager

import spotifyCore

currSongThread = None
currSongInfo = None

game_guessing_client = None
game_guessing_button = False

game_guessing_userList = None

game_stats_userScore = {}
game_stats_wrongGuesses = {}
game_stats_rounds = 0

def game_start():
    global currSongThread
    global game_guessing_button
    global game_guessing_userList

    global game_stats_userScore
    global game_stats_wrongGuesses

    global game_stats_rounds

    # Stop spotify playback
    spotifyCore.player_pausePlayback()

    serverCore.server_status = 2

    # Send countdown message to all clients
    serverCore.send_msgToClients('[update_status]' + str(serverCore.server_status))
    serverCore.send_msgToClients('[game_status_start]10')

    # Update server menu
    menuManager.update_serverMenu(['> Game starts in 10 seconds...'])

    # Delay 10 seconds
    time.sleep(10)

    # Send countdown message to all clients
    serverCore.send_msgToClients('[game_status_start]0')

    # Update server menu
    menuManager.update_serverMenu(['> Game is starting now...'])

    # Set guessing client list
    game_guessing_userList = list(serverCore.server_connections.keys()).copy()

    # Set guessing client scores
    for username in list(serverCore.server_connections.keys()):
        game_stats_userScore[username] = 0
        game_stats_wrongGuesses[username] = 0

    # Send update stats
    game_sendStats()

    # Reset rounds played
    game_stats_rounds = 0

    # Update game status
    serverCore.server_status = 3
    serverCore.send_msgToClients('[update_status]' + str(serverCore.server_status))

    # Delay 1 second
    time.sleep(1)

    # Configure song playtime
    songDuration = game_setSpotifyPlayback(True)

    # Send info to clients
    game_guessing_button = True
    serverCore.send_msgToClients('[game_guessing_button]' + str(game_guessing_button))

    # Send song duration to clients
    serverCore.send_msgToClients('[game_song_duration]' + str(songDuration))
    serverCore.send_msgToClients('[game_round]newRound')

    # Create new thread with songDuration
    currSongThread = Thread(target=game_songPlayThread, args=(songDuration, ))
    currSongThread.start()

    # Open menuManager ingame menu
    input('')

def game_songPlayThread(songDuration):
    global currSongThread

    thisSongThread = currSongThread

    # Delay song duration
    time.sleep(songDuration)

    # Check if thread is should still run
    if(thisSongThread != currSongThread):
        return

    # Stop spotify playback
    spotifyCore.player_pausePlayback()

    # Start new round
    game_startNewRound('timeRanOut')

def handle_guess_request(clientConnection):
    global currSongThread
    global game_guessing_client
    global game_guessing_button

    # Check if guessing is enabled
    if(game_guessing_button == True):
        # Set clientConnection as guessing client
        game_guessing_client = clientConnection

        # Set guessing button to false
        game_guessing_button = False

        # Send info to all clients
        serverCore.send_msgToClients('[game_guessing_button]' + str(game_guessing_button))
        serverCore.send_msgToClients('[game_guessing_username]' + str(serverCore.get_username(clientConnection)))

        # Send info to client
        serverCore.send_clientMsg(clientConnection, '[client_guess_accept]' + str(serverCore.opt_guessTime))

        # Stop spotify playback
        spotifyCore.player_pausePlayback()

        # Set currThread to guessTime sec timer
        currSongThread = Thread(target=game_userGuessThread, args=( ))
        currSongThread.start()


def handle_guess_input(clientConnection, guessInput):
    global currSongInfo
    global currSongThread
    global game_guessing_button
    global game_stats_userScore
    global game_stats_wrongGuesses
    global game_stats_rounds

    # Check if guessInput equals songName
    if(((serverCore.opt_guessTitle == True and serverCore.opt_guessArtist == False) and (game_checkTitleGuess(currSongInfo['item']['name'], guessInput) == True)) or ((serverCore.opt_guessArtist == True and serverCore.opt_guessTitle == False) and (game_checkArtistGuess(currSongInfo['item']['artists'], guessInput) == True)) or ((serverCore.opt_guessArtist == True and serverCore.opt_guessTitle == True) and ((game_checkArtistGuess(currSongInfo['item']['artists'], guessInput) == True) and (game_checkTitleGuess(currSongInfo['item']['name'], guessInput) == True)))):
        # GuessInput match
        
        # Increase users wins
        game_stats_userScore[serverCore.get_username(clientConnection)] += 1
        
        # Send update stats
        game_sendStats()
        
        # Check if user won the game
        if(game_stats_userScore[serverCore.get_username(clientConnection)] == serverCore.opt_winScore):

            # Cancel song thread
            currSongThread = None

            # Get song artist names
            songArtists = ''

            currArtist = 0
            for artistInfo in currSongInfo['item']['artists']:
                currArtist += 1
                songArtists += re.sub(r'[^\x00-\x7f]',r'?', artistInfo['name'])

                if(currArtist != len(currSongInfo['item']['artists'])):
                    songArtists += ' & '

            game_guessing_button = False

            # Send info to clients
            serverCore.send_msgToClients('[game_song_name]' + re.sub(r'[^\x00-\x7f]',r'?', str(currSongInfo['item']['name'])))
            serverCore.send_msgToClients('[game_song_artists]' + songArtists)
            serverCore.send_msgToClients('[game_guessing_button]' + str(game_guessing_button))
            serverCore.send_msgToClients('[game_round]userWon')

            # Increase rounds played
            game_stats_rounds += 1

            # Wait 2 seconds
            time.sleep(2)

            # Play refrain
            game_playSpotifyRefrain()

            # Wait 2 seconds
            time.sleep(2)

            serverCore.send_msgToClients('[game_stats_game]' + str(game_stats_rounds))

            serverCore.server_status = 4

            # Send countdown message to all clients
            serverCore.send_msgToClients('[update_status]' + str(serverCore.server_status))
            return
        
        # Start new round
        game_startNewRound('correctGuess')
        
    else:
        # GuessInput dosnt equals
        # Remove user from guessing list
        game_guessing_userList.remove(serverCore.get_username(clientConnection))

        # Increase users wrong guesses
        game_stats_wrongGuesses[serverCore.get_username(clientConnection)] += 1

        # Send update stats
        game_sendStats()

        # Check if all users have guessed
        if(len(game_guessing_userList) == 0):
            # Start new round
            game_startNewRound('allUsersGuessed')

            return

        # Configure song playtime
        songDuration = game_setSpotifyPlayback(False)

        # Send info to clients
        game_guessing_button = True
        serverCore.send_msgToClients('[game_guessing_button]' + str(game_guessing_button))

        # Send song duration to clients
        serverCore.send_msgToClients('[game_song_duration]' + str(songDuration))
        serverCore.send_msgToClients('[game_round]continueGuessing')

        # Create new thread with songDuration
        currSongThread = Thread(target=game_songPlayThread, args=(songDuration, ))
        currSongThread.start()


def game_userGuessThread():
    global currSongThread
    global game_guessing_button
    global game_guessing_userList
    global game_guessing_client
    global game_stats_userScore
    global game_stats_wrongGuesses

    thisSongThread = currSongThread

    # Delay guessTime seconds
    time.sleep(serverCore.opt_guessTime)

    # Check if thread is should still run
    if(thisSongThread != currSongThread):
        return

    # Remove user from guessing list
    game_guessing_userList.remove(serverCore.get_username(game_guessing_client))

    # Increase users wrong guesses
    game_stats_wrongGuesses[serverCore.get_username(game_guessing_client)] += 1
    
    # Send update stats
    game_sendStats()

    # Check if all users have guessed
    if(len(game_guessing_userList) == 0):
        # Start new round
        game_startNewRound('allUsersGuessed')

        return

    # Configure song playtime
    songDuration = game_setSpotifyPlayback(False)

    # Send info to clients
    game_guessing_button = True
    serverCore.send_msgToClients('[game_guessing_button]' + str(game_guessing_button))

    # Send song duration to clients
    serverCore.send_msgToClients('[game_song_duration]' + str(songDuration))
    serverCore.send_msgToClients('[game_round]continueGuessing')

    # Create new thread with songDuration
    currSongThread = Thread(target=game_songPlayThread, args=(songDuration, ))
    currSongThread.start()

def game_sendStats():
    global game_stats_userScore
    global game_stats_wrongGuesses

    for username in list(serverCore.server_connections.keys()):
        serverCore.send_msgToClients('[game_stats_user]' + username + '-|-' + str(game_stats_userScore[username]) + '-|-' + str(game_stats_wrongGuesses[username]))

def game_setSpotifyPlayback(newRound):
    global currSongInfo

    # Check for new round
    if(newRound):
        # Spotify skip song
        spotifyCore.player_skipPlayback()

        # Stop spotify playback
        spotifyCore.player_pausePlayback()

    time.sleep(1)

    # Get SongInfo
    currSongInfo = spotifyCore.player_currentSong()

    # Check for game mode
    if(serverCore.opt_gamemode == 0):
        # Normal 
        # Calc time position
        songNewPos = (currSongInfo['item']['duration_ms'] * serverCore.opt_timer) - currSongInfo['progress_ms']

        # Resume playback
        spotifyCore.player_resumePlayback()

        # Return playtime in seconds
        return (songNewPos / 1000)

    elif(serverCore.opt_gamemode == 1):
        # Speed 
        if(newRound):
            # Calc time position
            songTimeHalf = int(currSongInfo['item']['duration_ms']) / 2
            songNewPos = songTimeHalf - ((currSongInfo['item']['duration_ms'] * serverCore.opt_timer) / 2)

            # Seek playback to pos
            spotifyCore.player_seekPosition(songNewPos)

        # Resume playback
        spotifyCore.player_resumePlayback()

        # Return playtime in seconds
        return (((currSongInfo['item']['duration_ms'] * serverCore.opt_timer) - currSongInfo['progress_ms']) / 1000)

def game_playSpotifyRefrain():
    global currSongInfo

    # Check if playRefrain is on
    if(serverCore.opt_playRefrain == False):
        return

    # Calc time position
    songTimeHalf = int(currSongInfo['item']['duration_ms']) / 2
    songNewPos = songTimeHalf - ((currSongInfo['item']['duration_ms'] * 0.05) / 2)

    # Seek playback to pos
    spotifyCore.player_seekPosition(songNewPos)

    # Resume playback
    spotifyCore.player_resumePlayback()

    # Wait time
    time.sleep((currSongInfo['item']['duration_ms'] * 0.05) / 1000)

    # Pause playback
    spotifyCore.player_pausePlayback()


def game_startNewRound(endReason):
    global currSongInfo
    global game_guessing_button
    global game_guessing_userList
    global currSongThread
    global game_stats_rounds

    # Cancel song thread
    currSongThread = None

    # Get song artist names
    songArtists = ''

    currArtist = 0
    for artistInfo in currSongInfo['item']['artists']:
        currArtist += 1
        songArtists += re.sub(r'[^\x00-\x7f]',r'?', artistInfo['name'])

        if(currArtist != len(currSongInfo['item']['artists'])):
            songArtists += ' & '

    game_guessing_button = False

    # Send info to clients
    serverCore.send_msgToClients('[game_song_name]' + re.sub(r'[^\x00-\x7f]',r'?', str(currSongInfo['item']['name'])))
    serverCore.send_msgToClients('[game_song_artists]' + songArtists)
    serverCore.send_msgToClients('[game_guessing_button]' + str(game_guessing_button))
    serverCore.send_msgToClients('[game_round]' + endReason)

    # Increase rounds played
    game_stats_rounds += 1

    # Wait 2 seconds
    time.sleep(2)

    # Play refrain
    game_playSpotifyRefrain()

    # Wait 2 seconds
    time.sleep(2)

    # Set guessing client list
    game_guessing_userList = list(serverCore.server_connections.keys()).copy()

    # Configure song playtime
    songDuration = game_setSpotifyPlayback(True)

    # Send info to clients
    game_guessing_button = True
    serverCore.send_msgToClients('[game_guessing_button]' + str(game_guessing_button))

    # Send song duration to clients
    serverCore.send_msgToClients('[game_song_duration]' + str(songDuration))
    serverCore.send_msgToClients('[game_round]newRound')

    # Create new thread with songDuration
    currSongThread = Thread(target=game_songPlayThread, args=(songDuration, ))
    currSongThread.start()

def game_checkTitleGuess(songTitle, userGuess):
    correctGuess = True

    # Ignore case
    if(serverCore.opt_ignoreCase == True):
        songTitle = songTitle.lower()
        userGuess = userGuess.lower()

    songWords = []
    userWords = []

    # Transform songTitle to list
    for currWord in songTitle.split(' '):
        
        # Ignore additional
        if(serverCore.opt_ignoreAdd) == True:
            if(('-' in currWord or '(' in currWord or ')' in currWord or '[' in currWord) and len(songWords) > 0):
                break

        # Ignore special chars
        if(serverCore.opt_ignoreSpecial == True):
            currWord = re.sub(r'[^a-zA-Z0-9]', '', currWord) #''.join(filter(str.isalpha, currWord))

        if(currWord == None or currWord == ''):
            continue

        # Add currWord to list
        songWords += [currWord]

    # Transform userGuess to list
    for currWord in userGuess.split(' '):
        
        # Ignore additional
        if(serverCore.opt_ignoreAdd) == True:
            if(('-' in currWord or '(' in currWord or ')' in currWord or '[' in currWord) and len(userWords) > 0):
                break

        # Ignore special chars
        if(serverCore.opt_ignoreSpecial == True):
            currWord = re.sub(r'[^a-zA-Z0-9]', '', currWord) #''.join(filter(str.isalpha, currWord))

        if(currWord == None or currWord == ''):
            continue

        # Add currWord to list
        userWords += [currWord]

    # Ignore order
    if(serverCore.opt_ignoreOrder == True):
        # Check for each songWord if it is in userWords
        for currWord in songWords:
            if(not (currWord in userWords)):
                correctGuess = False
                break
    
    else:
        # Check for each songWord if it is in userWords
        if(not (songWords[0] in userWords)):
            correctGuess = False
        else:
            i = 0
            for currWord in userWords:
                if(currWord == songWords[0]):
                    for currSongWord in songWords:
                        if((len(userWords) < (i+1)) or not (userWords[i] == currSongWord)):
                            correctGuess = False
                            break
                        i += 1
                i += 1

    return correctGuess

def game_checkArtistGuess(songArtistsRaw, userGuess):
    correctGuess = True

    songArtists = []
    userArtists = []

    # Ignore Features
    if(serverCore.opt_ignoreFeatures == True):
        for currArtistWord in songArtistsRaw[0]['name'].split(' '):
            # Ignore special character
            if(serverCore.opt_ignoreSpecial == True):
                # Ignore case
                if(serverCore.opt_ignoreCase == True):
                    songArtists += [re.sub(r'[^a-zA-Z0-9]', '', currArtistWord).lower()]
                else:
                    songArtists += [re.sub(r'[^a-zA-Z0-9]', '', currArtistWord)]
            else:
                # Ignore case
                if(serverCore.opt_ignoreCase == True):
                    songArtists += [currArtistWord.lower()]
                else:
                    songArtists += [currArtistWord]
    else:
        for artistInfo in songArtistsRaw:
            for currArtistWord in artistInfo['name'].split(' '):
                # Ignore special character
                if(serverCore.opt_ignoreSpecial == True):
                    # Ignore case
                    if(serverCore.opt_ignoreCase == True):
                        songArtists += [re.sub(r'[^a-zA-Z0-9]', '', currArtistWord).lower()]
                    else:
                        songArtists += [re.sub(r'[^a-zA-Z0-9]', '', currArtistWord)]
                else:
                    # Ignore case
                    if(serverCore.opt_ignoreCase == True):
                        songArtists += [currArtistWord.lower()]
                    else:
                        songArtists += [currArtistWord]
            
    # Split user guess
    for userArtistGuess in userGuess.split(' '):
        # Ignore special character
        if(serverCore.opt_ignoreSpecial == True):
            # Ignore case
            if(serverCore.opt_ignoreCase == True):
                userArtists += [re.sub(r'[^a-zA-Z0-9]', '', userArtistGuess).lower()]
            else:
                userArtists += [re.sub(r'[^a-zA-Z0-9]', '', userArtistGuess)]
        else:
            # Ignore case
            if(serverCore.opt_ignoreCase == True):
                userArtists += [userArtistGuess.lower()]
            else:
                userArtists += [userArtistGuess]

    # Check for each songArtist if it is in userArtists
    for currArtist in songArtists:
        if(not (currArtist in userArtists)):
            correctGuess = False
            break

    return correctGuess

        