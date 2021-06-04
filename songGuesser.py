import fileCore

import menuManager

import serverCore
import clientCore
import spotifyCore

import requests, os, subprocess

import random

VERSION = 'v0.1.0'

def main():

    # Load Files
    fileCore.load_spotifyToken()
    fileCore.load_settings()

    # Choose between server and client mode
    print('> Choose application mode')
    print('> [1] Client Mode')
    print('> [2] Server Mode')

    # Check input
    appMode = input('> Please enter mode number (1): ')

    # Check if mode is 1 or 2
    if(appMode == '2'):
        # Server mode
        print('- - - - -')
        print('> Starting in Server Mode...')
        print('> Connecting to Spotify...')

        # Get spotify client id
        if(spotifyCore.CLIENT_ID == None or spotifyCore.CLIENT_SECRET == None):
            print(' ')
            print('> Please enter your Spotify clientID and clientSecret...')
            print('> This information is stored and can be changed in the \"config/settings.txt\" file')

            while(spotifyCore.CLIENT_ID == None):
                input_clientID = input('> Enter your Spotify ClientID: ')
                if(input_clientID != None and input_clientID.replace(' ', '') != ''):
                    spotifyCore.CLIENT_ID = str(input_clientID.replace(' ', '').replace('\n',''))
                else: 
                    print('> Wrong input... please try again')

            while(spotifyCore.CLIENT_SECRET == None):
                input_clientSecret = input('> Enter your Spotify ClientSecret: ')
                if(input_clientSecret != None and input_clientSecret.replace(' ', '') != ''):
                    spotifyCore.CLIENT_SECRET = str(input_clientSecret.replace(' ', '').replace('\n',''))
                else: 
                    print('> Wrong input... please try again')

            fileCore.save_settings()

            print('> Successfully updated your Spotify information')


        # Start server
        serverCore.start_server(1233)

        # Show server main menu
        menuManager.show_serverMainMenu(None)

    else:
        # Client mode
        print('- - - - -')
        print('> Starting in Client Mode...')

        # Input ip address
        server_IP = input('> Please enter the ip-address (Example: 192.199.1.123 ): ').replace(' ', '')

        # Input port
        server_Port = int(input('> Please enter the port (Default: 1233 ): ').replace(' ', ''))

        # Choose username
        clientCore.client_username = input('> Please enter username: ').replace(' ', '_')[0:12]

        if(clientCore.client_username == ''):
            # Generate random username
            clientCore.client_username = 'Client_' + str(random.randint(1, 99999))
        

        clientCore.start_client(server_IP, server_Port)

        menuManager.show_clientMainMenu(None)


# Start Program
print('---  Song Guesser  ---')
print('<-- Version ' + VERSION + ' -->')
print('<--  by spiegelei  -->')
print(' ')

# Check version
print('> Checking for new version...')

try:
    username = "lordspiegelei"
    # url to request
    url = f"https://api.github.com/repos/{username}/songGuesser-py/releases/latest"
    # make the request and return the json
    repo_info = requests.get(url).json()

    if(not 'tag_name' in repo_info.keys()):
        print('> No releases found...')
    else:
        if(repo_info["tag_name"] == VERSION):
            print('> Your version is the newest. No updates available!')
        else:
            print('<-- A new version is available -->')
            print('> The newest version is ' + repo_info['tag_name'])
            print('> Do you want to update now? (Yes/No)')

            update_awnser = input()

            if(update_awnser.lower() == 'yes' or update_awnser.lower() == 'y'):
                print('> Starting update...')
                subprocess.Popen(['python', os.path.dirname(__file__) + '\\updateVersion.py'])
                quit(0)

            else:
                print('> It is recommended to update as soon as possible...')
                print('> https://github.com/LordSpiegelei/songGuesser-py/releases/latest')

except Exception as e:
    print('> Version check failed')
    print(e)

print(' ')
print('- - - - -')
print(' ')

main()