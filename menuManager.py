import os
import threading
import serverCore
import clientCore
import gameManager
import spotifyCore
import re

currentMenu = 0
currMenuMessages = None
inputRunning = False

def clearConsole(): os.system('cls') #on Windows System

def show_serverMainMenu(infoMessages):
    global currentMenu

    currentMenu = 1

    # Print spotify info
    spotify_userInfo = spotifyCore.get_userInfo(False)

    # Clear console
    clearConsole()

    print(' ')
    print('<--<[ Spotify Info ]>-->')
    print('> Username: ' + spotify_userInfo['display_name'])
    print('> ID: ' + spotify_userInfo['id'])
    print('> Product: ' + spotify_userInfo['product'])
    print(' ')

    # Print menu options
    print('<--<[ Server Status ]>-->')
    print('> Status: ' + str(serverCore.server_status))
    print('> Clients: ' + str(serverCore.server_clientCount))
    print(' ')
    print('<--<[ Server Actions ]>-->')
    print('> [1] Settings')
    print('> [2] List Clients')
    print('> [3] Start')
    print('> [4] Stop')

    # Add in info message
    if(infoMessages != None and infoMessages != ''):
        print('<--<[ Info ]>-->')
        # For each message
        for infoMsg in infoMessages:
            print(infoMsg)

    # Listen for input
    actionInput = input('> Choose an action: ')

    # Check Input
    if(actionInput == '1'):
        # Open serverSettings
        show_serverSettingsMenu(infoMessages)

    elif(actionInput == '2'):
        # open serverClientsMenu
        show_serverClientsMenu(infoMessages)

    elif(actionInput == '3'):
        # Start server
        # Check if enough users are connected
        if(serverCore.server_clientCount >= 2):
            # Enough clients connected
            gameManager.game_start()
        else:
            # Not enough clients
            show_serverMainMenu(['> Not able to start game... there are less then 2 clients connected!'])

    elif(actionInput == '4'):
        # Stop server
        serverCore.SERVER_RUNNING = False

    else:
        # Reopen menu
        show_serverMainMenu(infoMessages)

def show_serverSettingsMenu(infoMessages):
    global currentMenu

    currentMenu = 2

    # Clear console
    clearConsole()

    # Print menu options
    print('<--<[ Server Settings ]>-->')
    print('> [1] Moderator (' + str(serverCore.opt_moderator) + ')')
    print('> [2] GameMode (' + str(serverCore.opt_gamemode) + ')')
    print('> [3] Song Duration (' + str(serverCore.opt_timer) + ')')
    print('> [4] Guessing Time (' + str(serverCore.opt_guessTime) + ')')
    print('> [5] Play Refrain (' + str(serverCore.opt_playRefrain) + ')')
    print('> [6] Win Score (' + str(serverCore.opt_winScore) + ')')
    print(' ')
    print('> [7] Guess Title (' + str(serverCore.opt_guessTitle) + ')')
    print('> [8] Guess Artist (' + str(serverCore.opt_guessArtist) + ')')
    print(' ')
    print('> [9] Ignore Case (' + str(serverCore.opt_ignoreCase) + ')')
    print('> [10] Ignore Order (' + str(serverCore.opt_ignoreOrder) + ')')
    print('> [11] Ignore Special (' + str(serverCore.opt_ignoreSpecial) + ')')
    print('> [12] Ignore Additional (' + str(serverCore.opt_ignoreAdd) + ')')
    print(' ')
    print('> [13] Ignore Features (' + str(serverCore.opt_ignoreAdd) + ')')
    print(' ')
    print('> [14] Go Back')

    # Add in info message
    if(infoMessages != None and infoMessages != ''):
        print('<--<[ Info ]>-->')
        # For each message
        for infoMsg in infoMessages:
            print(infoMsg)

    # Listen for input
    actionInput = input('> Choose an setting: ')

    # Check Input
    if(actionInput == '1'):
        # Edit moderator
        editInput = input('> Edit Moderator [Bot/User] (Bot): ')

        # Check Input
        if(editInput.lower() == 'user'):
            # Change moderator to user
            serverCore.opt_moderator = 1

            # Reopen settingsMenu
            show_serverSettingsMenu(infoMessages)
        else:
            # Change moderator to bot
            serverCore.opt_moderator = 0

            # Reopen settingsMenu
            show_serverSettingsMenu(infoMessages)
    
    elif(actionInput == '2'):
        # Edit gameMode
        editInput = input('> Edit GameMode [Normal/Speed] (Normal): ')

        # Check Input
        if(editInput.lower() == 'speed'):
            # Change gameMode to speed
            serverCore.opt_gamemode = 1

            # Reopen settingsMenu
            show_serverSettingsMenu(infoMessages)
        else:
            # Change gameMode to normal
            serverCore.opt_gamemode = 0

            # Reopen settingsMenu
            show_serverSettingsMenu(infoMessages)
    
    elif(actionInput == '3'):
        # Edit Timer
        editInput = input('> Edit Song Duration [Custom] (0.1): ')

        # Check Input
        if(editInput.replace(' ', '') == ''):
            # Change timer to (0.1)
            serverCore.opt_timer = 0.1

            # Reopen settingsMenu
            show_serverSettingsMenu(infoMessages)
        
        else:
            # Change timer to input
            serverCore.opt_timer = float(editInput)

            # Reopen settingsMenu
            show_serverSettingsMenu(infoMessages)
    
    elif(actionInput == '4'):
        # Edit max guesses
        editInput = input('> Edit Guessing Time [Custom] (30): ')

        # Check Input
        if(editInput.replace(' ', '') == ''):
            # Change max guesses to 30
            serverCore.opt_guessTime = 30

            # Reopen settingsMenu
            show_serverSettingsMenu(infoMessages)
        
        else:
            # Change max guesses to input
            serverCore.opt_guessTime = int(editInput)

            # Reopen settingsMenu
            show_serverSettingsMenu(infoMessages)
    elif(actionInput == '5'):
        # Edit
        editInput = input('> Edit Play Refrain [On/Off] (On): ')
        # Check Input
        if(editInput.lower() == 'off'):
            serverCore.opt_playRefrain = False
            # Reopen settingsMenu
            show_serverSettingsMenu(infoMessages)
        
        else:
            serverCore.opt_playRefrain = True
            # Reopen settingsMenu
            show_serverSettingsMenu(infoMessages)
    elif(actionInput == '6'):
        # Edit
        editInput = input('> Edit Win Score [Custom] (10): ')
        # Check Input
        if(editInput.replace(' ', '') == ''):
            # Change max guesses to 10
            serverCore.opt_winScore = 10

            # Reopen settingsMenu
            show_serverSettingsMenu(infoMessages)
        
        else:
            # Change max guesses to input
            serverCore.opt_winScore = int(editInput)

            # Reopen settingsMenu
            show_serverSettingsMenu(infoMessages)
    elif(actionInput == '7'):
        # Edit
        editInput = input('> Edit Guess Title [On/Off] (On): ')
        # Check Input
        if(editInput.lower() == 'off'):
            serverCore.opt_guessTitle = False
            # Reopen settingsMenu
            show_serverSettingsMenu(infoMessages)
        
        else:
            serverCore.opt_guessTitle = True
            # Reopen settingsMenu
            show_serverSettingsMenu(infoMessages)
    elif(actionInput == '8'):
        # Edit
        editInput = input('> Edit Guess Artist [On/Off] (Off): ')
        # Check Input
        if(editInput.lower() == 'on'):
            serverCore.opt_guessArtist = True
            # Reopen settingsMenu
            show_serverSettingsMenu(infoMessages)
        
        else:
            serverCore.opt_guessArtist = False
            # Reopen settingsMenu
            show_serverSettingsMenu(infoMessages)
    elif(actionInput == '9'):
        # Edit
        editInput = input('> Edit Ignore Case [On/Off] (On): ')
        # Check Input
        if(editInput.lower() == 'off'):
            serverCore.opt_ignoreCase = False
            # Reopen settingsMenu
            show_serverSettingsMenu(infoMessages)
        
        else:
            serverCore.opt_ignoreCase = True
            # Reopen settingsMenu
            show_serverSettingsMenu(infoMessages)
    elif(actionInput == '10'):
        # Edit
        editInput = input('> Edit Ignore Order [On/Off] (On): ')
        # Check Input
        if(editInput.lower() == 'off'):
            serverCore.opt_ignoreOrder = False
            # Reopen settingsMenu
            show_serverSettingsMenu(infoMessages)
        
        else:
            serverCore.opt_ignoreOrder = True
            # Reopen settingsMenu
            show_serverSettingsMenu(infoMessages)
    elif(actionInput == '11'):
        # Edit
        editInput = input('> Edit Ignore Special [On/Off] (On): ')
        # Check Input
        if(editInput.lower() == 'off'):
            serverCore.opt_ignoreSpecial = False
            # Reopen settingsMenu
            show_serverSettingsMenu(infoMessages)
        
        else:
            serverCore.opt_ignoreSpecial = True
            # Reopen settingsMenu
            show_serverSettingsMenu(infoMessages)
    elif(actionInput == '12'):
        # Edit
        editInput = input('> Edit Ignore Additional [On/Off] (On): ')
        # Check Input
        if(editInput.lower() == 'off'):
            serverCore.opt_ignoreAdd = False
            # Reopen settingsMenu
            show_serverSettingsMenu(infoMessages)
        
        else:
            serverCore.opt_ignoreAdd = True
            # Reopen settingsMenu
            show_serverSettingsMenu(infoMessages)
    elif(actionInput == '13'):
        # Edit
        editInput = input('> Edit Ignore Features [On/Off] (On): ')
        # Check Input
        if(editInput.lower() == 'off'):
            serverCore.opt_ignoreFeatures = False
            # Reopen settingsMenu
            show_serverSettingsMenu(infoMessages)
        
        else:
            serverCore.opt_ignoreFeatures = True
            # Reopen settingsMenu
            show_serverSettingsMenu(infoMessages)
    elif(actionInput == '14'):
        # Go Back
        # Show main menu
        show_serverMainMenu(infoMessages)
    else:
        # Reopen settings menu
        show_serverSettingsMenu(infoMessages)

def show_serverClientsMenu(infoMessages):
    global currentMenu

    currentMenu = 3

    # Clear console
    clearConsole()

   # Print menu options
    print('<--<[ Connected Clients ]>-->')

    clientActions = {}
    currClientNumb = 0

    for username in serverCore.server_connections.keys():
        currClientNumb += 1

        # Add current clients to clientActions
        clientActions[currClientNumb] = serverCore.server_connections[username]

        # Check if users is self
        print('> [' + str(currClientNumb) + '] ' + username)

    print(' ')
    print('<--<[ Server Actions ]>-->')
    print('> [' + str(currClientNumb + 1) + '] Go Back')

    # Add in info message
    if(infoMessages != None and infoMessages != ''):
        print('<--<[ Info ]>-->')
        # For each message
        for infoMsg in infoMessages:
            print(infoMsg)

    # Listen for input
    actionInput = input('> Choose an action: ')
 
    # Check Input
    if(actionInput == str(currClientNumb + 1)):
        # Go Back
        # Show main menu
        show_serverMainMenu(infoMessages)
    else:
        # Reopen client menu
        show_serverClientsMenu(infoMessages)

def update_serverMenu(infoMessages):
    global currentMenu

    if(currentMenu == 1):

        # Print spotify info
        spotify_userInfo = spotifyCore.get_userInfo(False)

        # Clear console
        clearConsole()

        print(' ')
        print('<--<[ Spotify Info ]>-->')
        print('> Username: ' + spotify_userInfo['display_name'])
        print('> ID: ' + spotify_userInfo['id'])
        print('> Product: ' + spotify_userInfo['product'])
        print(' ')

        # Print menu options
        print('<--<[ Server Status ]>-->')
        print('> Status: ' + str(serverCore.server_status))
        print('> Clients: ' + str(serverCore.server_clientCount))
        print(' ')
        print('<--<[ Server Actions ]>-->')
        print('> [1] Settings')
        print('> [2] List Clients')
        print('> [3] Start')
        print('> [4] Stop')

        # Add in info message
        if(infoMessages != None and infoMessages != ''):
            print('<--<[ Info ]>-->')
            # For each message
            for infoMsg in infoMessages:
                print(infoMsg)

        print('> Choose an action: ')

    elif(currentMenu == 2):

        # Clear console
        clearConsole()

        # Print menu options
        print('<--<[ Server Settings ]>-->')
        print('> [1] Moderator (' + str(serverCore.opt_moderator) + ')')
        print('> [2] GameMode (' + str(serverCore.opt_gamemode) + ')')
        print('> [3] Song Duration (' + str(serverCore.opt_timer) + ')')
        print('> [4] Guessing Time (' + str(serverCore.opt_guessTime) + ')')
        print('> [5] Play Refrain (' + str(serverCore.opt_playRefrain) + ')')
        print('> [6] Win Score (' + str(serverCore.opt_winScore) + ')')
        print(' ')
        print('> [7] Guess Title (' + str(serverCore.opt_guessTitle) + ')')
        print('> [8] Guess Artist (' + str(serverCore.opt_guessArtist) + ')')
        print(' ')
        print('> [9] Ignore Case (' + str(serverCore.opt_ignoreCase) + ')')
        print('> [10] Ignore Order (' + str(serverCore.opt_ignoreOrder) + ')')
        print('> [11] Ignore Special (' + str(serverCore.opt_ignoreSpecial) + ')')
        print('> [12] Ignore Additional (' + str(serverCore.opt_ignoreAdd) + ')')
        print(' ')
        print('> [13] Ignore Features (' + str(serverCore.opt_ignoreAdd) + ')')
        print(' ')
        print('> [15] Go Back')

        # Add in info message
        if(infoMessages != None and infoMessages != ''):
            print('<--<[ Info ]>-->')
            # For each message
            for infoMsg in infoMessages:
                print(infoMsg)

        print('> Choose an setting: ')

    elif(currentMenu == 3):

        # Clear console
        clearConsole()

        # Print menu options    
        print('<--<[ Connected Clients ]>-->')

        clientActions = {}
        currClientNumb = 0

        for username in serverCore.server_connections.keys():
            currClientNumb += 1

            # Add current clients to clientActions
            clientActions[currClientNumb] = serverCore.server_connections[username]

            # Check if users is self
            print('> [' + str(currClientNumb) + '] ' + username)

        print(' ')
        print('<--<[ Server Actions ]>-->')
        print('> [' + str(currClientNumb + 1) + '] Go Back')

        # Add in info message
        if(infoMessages != None and infoMessages != ''):
            print('<--<[ Info ]>-->')
            # For each message
            for infoMsg in infoMessages:
                print(infoMsg)

        print('> Choose an action: ')

def show_clientMainMenu(infoMessages):
    global currentMenu
    global inputRunning
    global currMenuMessages

    currentMenu = 1

    # Clear console
    clearConsole()

    # Print menu options
    print('<--<[ Game Status ]>-->')
    print('> Status: ' + str(clientCore.client_gameStatus)) 
    print('> Clients: ' + str(clientCore.client_clientCount))
    print('> Username: ' + str(clientCore.client_username))
    print(' ')
    print('<--<[ User Actions ]>-->')
    print('> [1] Change Username')
    print('> [2] List Clients')

    # Add in info message
    if(infoMessages != None and infoMessages != ''):
        print('<--<[ Info ]>-->')
        # For each message
        for infoMsg in infoMessages:
            print(infoMsg)

    # Listen for input
    currMenuMessages = infoMessages
    if(inputRunning):
        # Input is already running
        print('> Choose an action: ')
    else:
        # Create new input
        inputRunning = True
        handle_clientInput(input('> Choose an action: '))


def show_clientClientsMenu(infoMessages):
    global currentMenu
    global inputRunning
    global currMenuMessages

    currentMenu = 2

    # Clear console
    clearConsole()

   # Print menu options
    print('<--<[ Connected Users ]>-->')
    print(' ')

    for username in clientCore.client_connClients:
        # Check if user is self
        if(username == clientCore.client_username):
            print('> ' + username + ' [S]')
        else:
            print('> ' + username)

    print(' ')
    print('<--<[ User Actions ]>-->')
    print('> [1] Go Back')

    # Add in info message
    if(infoMessages != None and infoMessages != ''):
        print(' ')
        print('<--<[ Info ]>-->')
        print(' ')
        # For each message
        for infoMsg in infoMessages:
            print(infoMsg)

    print(' ')
    currMenuMessages = infoMessages
    if(inputRunning):
        # Input is already running
        print('> Choose an action: ')
    else:
        # Create new input
        inputRunning = True
        handle_clientInput(input('> Choose an action: '))


def show_clientGuessingMenu(infoMessages):
    global currentMenu
    global inputRunning
    global currMenuMessages

    currentMenu = 3

    # Clear console
    clearConsole()

    print('<--<[ Users ]>-->')
    print(' ')
    
    for username in list(clientCore.game_stats_userScore.keys()):
        # Get sspaces after username
        spaces = 12 - len(username)
        strSpaces = ''
        for i in range(0, spaces):
            strSpaces += ' '

        if(username == clientCore.game_guessing_username):
            print('>-> ' + username + strSpaces + ' ' + str(clientCore.game_stats_userScore[username]))
        else:
            print('> ' + username + strSpaces + '   ' + str(clientCore.game_stats_userScore[username]))

    # Add in info message
    if(infoMessages != None and infoMessages != ''):
        print(' ')
        print('<--<[ Info ]>-->')
        print(' ')
        # For each message
        for infoMsg in infoMessages:
            print(infoMsg)


    print(' ')
    print('<--<[ ]>-->')
    print(' ')

    currMenuMessages = infoMessages
    if(clientCore.game_guessing_guessed):
        # Handle
        if(inputRunning == True):
            print('> You already guessed this round! <')
        else:
            inputRunning = True
            print('> You already guessed this round! <')
            handle_clientInput(input(' '))
    elif(clientCore.game_guessing_button == True and clientCore.game_guessing_self == False):
        # Handle input
        if(inputRunning):
            print('>     Press ENTER to guess...     <')
        else:
            inputRunning = True
            print('>     Press ENTER to guess...     <')
            handle_clientInput(input(' '))
    elif(clientCore.game_guessing_button == False and clientCore.game_guessing_self == False):
        # Handle 
        if(inputRunning):
            print('> Guessing is currently disabled! <')
        else:
            inputRunning = True
            print('> Guessing is currently disabled! <')
            handle_clientInput(input(' '))
    elif(clientCore.game_guessing_self == True):
        # Handle input
        if(inputRunning):
            print('> Please enter your guess: ')
        else:
            inputRunning = True
            print('> Please enter your guess: ')
            handle_clientInput(input(' '))


def show_clientScoreboardMenu():
    global currentMenu
    global inputRunning
    global currMenuMessages

    currentMenu = 4

    # Clear console
    clearConsole()

    print('<--<[ Scoreboard ]>-->')
    print(' ')
    
    for username in list(clientCore.game_stats_userScore.keys()):
        # Get sspaces after username
        spaces = 12 - len(username)
        winSpaces = 2 - len(clientCore.game_stats_userScore[username])
        wrongSpaces = 2 - len(clientCore.game_stats_wrongGuesses[username])
        strSpaces = ''
        strWinSpaces = ''
        strWrongSpaces = ''
        for i in range(0, spaces):
            strSpaces += ' '

        for i in range(0, winSpaces):
            strWinSpaces += ' '

        for i in range(0, wrongSpaces):
            strWrongSpaces += ' '

        if(username == clientCore.game_guessing_username):
            print('>-> ' + username + strSpaces + ' ' + str(clientCore.game_stats_userScore[username]) + strWinSpaces + ' Wins - ' + str(clientCore.game_stats_wrongGuesses[username]) + strWrongSpaces + ' Wrong Guesses')
        else:
            print('> ' + username + strSpaces + '   ' + str(clientCore.game_stats_userScore[username]) + strWinSpaces + ' Wins - ' + str(clientCore.game_stats_wrongGuesses[username]) + strWrongSpaces + ' Wrong Guesses')

    print(' ')
    print('> The user ' + clientCore.game_guessing_username + ' won the game!')


def update_clientMenu(infoMessages):
    global currentMenu
    global currMenuMessages

    if(currentMenu == 1):
        # Clear console
        clearConsole()

        # Print menu options
        print('<--<[ Game Status ]>-->')
        print('> Status: ' + str(clientCore.client_gameStatus))
        print('> Clients: ' + str(clientCore.client_clientCount))
        print('> Username: ' + str(clientCore.client_username))
        print(' ')
        print('<--<[ User Action ]>-->')
        print('> [1] Change Username')
        print('> [2] List Clients')

        # Add in info message
        if(infoMessages != None and infoMessages != ''):
            print('<--<[ Info ]>-->')
            # For each message
            for infoMsg in infoMessages:
                print(infoMsg)

        currMenuMessages = infoMessages
        print('> Choose an action: ')

    elif(currentMenu == 2):
        # Clear console
        clearConsole()

        # Print menu options    
        print('<--<[ Connected Users ]>-->')

        for username in clientCore.client_connClients:
            # Check if users is self
            if(username == clientCore.client_username):
                print('> ' + username + ' [SELF]')
            else:
                print('> ' + username)

        print(' ')
        print('<--<[ User Actions ]>-->')
        print('> [1] Go Back')

        # Add in info message
        if(infoMessages != None and infoMessages != ''):
            print('<--<[ Info ]>-->')
            # For each message
            for infoMsg in infoMessages:
                print(infoMsg)

        currMenuMessages = infoMessages
        print('> Choose an action: ')

    elif(currentMenu == 3):
        # Clear console
        clearConsole()

        print('<--<[ Users ]>-->')
        print(' ')
        
        for username in list(clientCore.game_stats_userScore.keys()):
            # Get sspaces after username
            spaces = 12 - len(username)
            strSpaces = ''
            for i in range(0, spaces):
                strSpaces += ' '

            if(username == clientCore.game_guessing_username):
                print('>-> ' + username + strSpaces + ' ' + str(clientCore.game_stats_userScore[username]))
            else:
                print('> ' + username + strSpaces + '   ' + str(clientCore.game_stats_userScore[username]))

        # Add in info message
        if(infoMessages != None and infoMessages != ''):
            print(' ')
            print('<--<[ Info ]>-->')
            print(' ')
            # For each message
            for infoMsg in infoMessages:
                print(infoMsg)


        print(' ')
        print('<--<[ ]>-->')
        print(' ')

        currMenuMessages = infoMessages
        if(clientCore.game_guessing_guessed):
            # Handle
            print('> You already guessed this round! <')
        elif(clientCore.game_guessing_button == True and clientCore.game_guessing_self == False):
            # Handle input
            print('>     Press ENTER to guess...     <')
        elif(clientCore.game_guessing_button == False and clientCore.game_guessing_self == False):
            # Handle 
            print('> Guessing is currently disabled! <')
        elif(clientCore.game_guessing_self == True):
            # Handle input
            print('> Please enter your guess: ')

    elif(currentMenu == 4):
        # Clear console
        clearConsole()

        print('<--<[ Scoreboard ]>-->')
        print(' ')
        
        for username in list(clientCore.game_stats_userScore.keys()):
            # Get sspaces after username
            spaces = 12 - len(username)
            winSpaces = 2 - len(clientCore.game_stats_userScore[username])
            wrongSpaces = 2 - len(clientCore.game_stats_wrongGuesses[username])
            strSpaces = ''
            strWinSpaces = ''
            strWrongSpaces = ''
            for i in range(0, spaces):
                strSpaces += ' '

            for i in range(0, winSpaces):
                strWinSpaces += ' '

            for i in range(0, wrongSpaces):
                strWrongSpaces += ' '

            if(username == clientCore.game_guessing_username):
                print('>-> ' + username + strSpaces + ' ' + str(clientCore.game_stats_userScore[username]) + strWinSpaces + ' Wins - ' + str(clientCore.game_stats_wrongGuesses[username]) + strWrongSpaces + ' Wrong Guesses')
            else:
                print('> ' + username + strSpaces + '   ' + str(clientCore.game_stats_userScore[username]) + strWinSpaces + ' Wins - ' + str(clientCore.game_stats_wrongGuesses[username]) + strWrongSpaces + ' Wrong Guesses')

        print(' ')
        print('> The user ' + clientCore.game_guessing_username + ' won the game!')

def handle_clientInput(inputMessage):
    global currentMenu
    global currMenuMessages
    global inputRunning

    inputRunning = False

    # Check currentMenu
    if(currentMenu == 1):
        # Check Input
        if(inputMessage == '1'):
            # Edit max guesses
            editInput = input('> Type in new username: ')

            # Check Input
            clientCore.client_username = editInput

            show_clientMainMenu(currMenuMessages)

        elif(inputMessage == '2'):
            # Show connected users menu
            show_clientClientsMenu(currMenuMessages)
            
        else:
            # Reopen client menu
            show_clientMainMenu(currMenuMessages)

    elif(currentMenu == 2): 
        # Check Input
        if(inputMessage == '1'):
            # Go Back
            # Show main menu
            show_clientMainMenu(currMenuMessages)
        else:
            # Reopen client menu
            show_clientClientsMenu(currMenuMessages)
    
    elif(currentMenu == 3):
        # Check Input
        if(clientCore.game_guessing_guessed):
            # User already guessed
            show_clientGuessingMenu(currMenuMessages)
        elif(clientCore.game_guessing_button and clientCore.game_guessing_self == False):
            # User guessing is enabled
            # Send guess request to server
            clientCore.send_message('[client_guess_request]')

            # Reopen menu
            show_clientGuessingMenu(currMenuMessages)
        elif(clientCore.game_guessing_button == False and clientCore.game_guessing_self == False):
            # User guessing is disabled

            # Reopen menu
            show_clientGuessingMenu(currMenuMessages)
        elif(clientCore.game_guessing_self):
            # User is guessing
            # Send guess input to server
            clientCore.send_message('[client_guess_input]' + re.sub(r'[^\x00-\x7f]',r'?', inputMessage))

            # Reopen menu
            show_clientGuessingMenu(currMenuMessages)
