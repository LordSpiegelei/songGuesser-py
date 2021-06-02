import socket
import struct
import time
from _thread import *

import menuManager

client_clientCount = 0
client_gameStatus = 0
client_username = 'NOT DEFINED'
client_connClients = []

game_song_duration = 0.0
game_song_name = ''
game_song_artists = ''
game_guessing_button = False
game_guessing_self = False
game_guessing_username = ''
game_guessing_guessed = False

game_stats_userScore = {}
game_stats_wrongGuesses = {}
game_stats_rounds = 0

CLIENT_SOCKET = None

def start_client():
    start_new_thread(client_thread, ())

def client_thread():
    global CLIENT_SOCKET

    global client_username

    CLIENT_SOCKET = socket.socket()
    host = '8.tcp.ngrok.io' #'127.0.0.1'
    port = 17564 #1233

    try:
        CLIENT_SOCKET.connect((host, port))
    except socket.error as e:
        print(str(e))

    # Send username to Server
    send_message('[client_username]' + client_username)

    # Handle client response
    while True:

        try:
            size = struct.unpack("i", CLIENT_SOCKET.recv(struct.calcsize("i")))[0]
            data = ""
            while len(data) < size:
                msg = CLIENT_SOCKET.recv(size - len(data)).decode('utf-8')
                if not msg:
                    continue
                data += msg

            handle_serverMessage(data)

        except OSError as e:
            print(e)
            quit()
        except Exception as e:
            print(e)
            quit()
    
    quit()
    #CLIENT_SOCKET.close()

def handle_serverMessage(server_message):
    global client_gameStatus
    global client_clientCount
    global client_connClients

    global game_song_duration
    global game_song_name
    global game_song_artists
    global game_guessing_button
    global game_guessing_self
    global game_guessing_username
    global game_guessing_guessed

    global game_stats_userScore
    global game_stats_wrongGuesses
    global game_stats_rounds

    # Check prefix of message
    if(server_message.startswith('[update_status]')):
        client_gameStatus = int(server_message.replace('[update_status]', ''))
        
        # Update client menu
        menuManager.update_clientMenu(None)

        if(client_gameStatus == 3):
            # New game is starting
            # Reset settings
            game_guessing_button = False
            game_guessing_self = False
            game_guessing_username = ''
            game_guessing_guessed = False

            # Open client guessing menu
            menuManager.show_clientGuessingMenu(['A new game is starting soon...'])

        elif(client_gameStatus == 4):
            # Game ended
            game_guessing_button = False
            game_guessing_self = False
            game_guessing_guessed = False

            # Open client scoreboard menu
            menuManager.show_clientScoreboardMenu()
    
    elif(server_message.startswith('[update_clientCount]')):
        client_clientCount = server_message.replace('[update_clientCount]', '')

        # Update client menu
        menuManager.update_clientMenu(None)

    elif(server_message.startswith('[update_connClients]')):
        connClientsRaw = server_message.replace('[update_connClients]', '')

        # Split raw
        client_connClients = connClientsRaw.split('[/split/]')

        # Update client menu
        menuManager.update_clientMenu(None)

    elif(server_message.startswith('[game_status_start]')):
        startTime = server_message.replace('[game_status_start]', '')

        # Check if start time is 10
        if(startTime == '10'):
            # Send countdown message
            menuManager.update_clientMenu(['> Game starts in 10 seconds...'])

            # Delay 5 seconds
            time.sleep(5)

            # Send countdown message
            menuManager.update_clientMenu(['> Game starts in 5 seconds...'])

            time.sleep(1)
            menuManager.update_clientMenu(['> Game starts in 4 seconds...'])

            time.sleep(1)
            menuManager.update_clientMenu(['> Game starts in 3 seconds...'])

            time.sleep(1)
            menuManager.update_clientMenu(['> Game starts in 2 seconds...'])

            time.sleep(1)
            menuManager.update_clientMenu(['> Game starts in 1 second...'])

        # Check if start time is 0
        elif(startTime == '0'):
            # Send starting message
            menuManager.update_clientMenu(['> Game is starting now...'])

    elif(server_message.startswith('[game_song_duration]')):
        game_song_duration = float(server_message.replace('[game_song_duration]', ''))

    elif(server_message.startswith('[game_song_name]')):
        game_song_name = server_message.replace('[game_song_name]', '')

    elif(server_message.startswith('[game_song_artists]')):
        game_song_artists = server_message.replace('[game_song_artists]', '')

    elif(server_message.startswith('[game_guessing_button]')): 
        game_guessing_button = eval(server_message.replace('[game_guessing_button]', ''))

    elif(server_message.startswith('[game_guessing_username]')): 
        game_guessing_username = server_message.replace('[game_guessing_username]', '')
        # Update menu
        menuManager.update_clientMenu(['User ' + game_guessing_username + ' is now guessing...'])

    elif(server_message.startswith('[game_stats_user]')): 
        # User stats update
        username = server_message.replace('[game_stats_user]', '').split('-|-')[0]
        userScore = server_message.replace('[game_stats_user]', '').split('-|-')[1]
        wrongGuesses = server_message.replace('[game_stats_user]', '').split('-|-')[2]
        
        # Add user to lists
        game_stats_userScore[username] = userScore
        game_stats_wrongGuesses[username] = wrongGuesses
        
    elif(server_message.startswith('[game_stats_game]')): 
        # User stats update
        roundsPlayed = server_message.replace('[game_stats_user]', '').split('-|-')[0]

        # Add user to lists
        game_stats_rounds = roundsPlayed

    elif(server_message.startswith('[game_round]')): 
        game_round = server_message.replace('[game_round]', '')

        # Check game round info
        if (game_round == 'newRound'):
            # New round
            game_guessing_self = False
            game_guessing_guessed = False
            game_guessing_username = None

            menuManager.update_clientMenu(['> Song plays for ' + str(game_song_duration) + ' seconds'])

        elif (game_round == 'continueGuessing'):
            # Continue guessing
            # Set user guessed to true
            if(game_guessing_self):
                game_guessing_guessed = True
                game_guessing_self = False

            game_guessing_username = None

            menuManager.update_clientMenu(['> Song plays for ' + str(game_song_duration) + ' seconds'])

        elif (game_round == 'timeRanOut'):
            # End round
            # Set user guessed to true
            if(game_guessing_self):
                game_guessing_guessed = True
                game_guessing_self = False

            game_guessing_username = None

            menuManager.update_clientMenu(['> Guessing time ran out! New round starting soon...', ' ', '>--> Song Info <--<', '> Name: ' + game_song_name, '> Artists: ' + game_song_artists])

        elif (game_round == 'allUsersGuessed'):
            # End round
            # Set user guessed to true
            if(game_guessing_self):
                game_guessing_guessed = True
                game_guessing_self = False

            game_guessing_username = None
            
            time.sleep(1)

            menuManager.update_clientMenu(['> All users have guessed! New round starting soon...', ' ', '>-->[ Song Info ]<--<', ' ', '> Name: ' + game_song_name, '> Artists: ' + game_song_artists])

        elif (game_round == 'correctGuess'):
            # End round
            # Set user guessed to true
            if(game_guessing_self):
                game_guessing_guessed = True
                game_guessing_self = False
            
            time.sleep(1)

            menuManager.update_clientMenu(['> Correct guess by ' + game_guessing_username + '!', ' ', '>-->[ Song Info ]<--<', ' ', '> Name: ' + game_song_name, '> Artists: ' + game_song_artists])

        elif (game_round == 'userWon'):
            # End round
            # Set user guessed to true
            if(game_guessing_self):
                game_guessing_guessed = True
                game_guessing_self = False
            
            time.sleep(1)

            menuManager.update_clientMenu(['> The user ' + game_guessing_username + ' won the game!', ' ', '>-->[ Song Info ]<--<', ' ', '> Name: ' + game_song_name, '> Artists: ' + game_song_artists])

    elif(server_message.startswith('[client_guess_accept]')):
        # Handle client guess accept
        game_guessDuration = server_message.replace('[client_guess_accept]', '')

        # Set self guessing true
        game_guessing_self = True

        # Update menu
        menuManager.update_clientMenu(['User ' + game_guessing_username + ' is now guessing...', 'You have ' + game_guessDuration + ' seconds to guess...'])

        
def send_message(message):
    global CLIENT_SOCKET

    try:
        msg = str.encode(message)
        CLIENT_SOCKET.send(struct.pack("i", len(msg)) + msg)
    except OSError as e:
        print(e)