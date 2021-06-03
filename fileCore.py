import spotifyCore
import os

FILEPATH_SPOTIFY = os.path.dirname(__file__) + '\\config\\spotifydata.data'
FILEPATH_SETTINGS = os.path.dirname(__file__) + '\\config\\settings.txt'

def checkPath():
    if(not os.path.isdir(os.path.dirname(__file__).replace('\\', '/') + '/config/')):
        os.mkdir(os.path.dirname(__file__).replace('\\', '/') + '/config/')

def load_spotifyToken():
    checkPath()

    if(not os.path.isfile(FILEPATH_SPOTIFY)):
        file = open(FILEPATH_SPOTIFY, 'w')
        file.close()
        return

    # Open File
    try:
        with open(FILEPATH_SPOTIFY, 'r') as file:
            # Read File Lines
            for line in file.readlines():
                # Read Token

                if(line.startswith('token=')):
                    spotifyCore.AUTH_TOKEN = line.replace('\n', '').replace('token=', '')
                elif(line.startswith('refresh_token=')):
                    spotifyCore.AUTH_REFRESH_TOKEN = line.replace('refresh_token=', '')
                
    except Exception as e:
        print(e)

def load_settings():
    checkPath()

    if(not os.path.isfile(FILEPATH_SETTINGS)):
        file = open(FILEPATH_SETTINGS, 'w')
        file.close()
        return

    # Open File
    try:
        with open(FILEPATH_SETTINGS, 'r') as file:
            # Read File Lines
            for line in file.readlines():
                # Read Settings

                if(line.startswith('spotify_client_id=')):
                    spotifyCore.CLIENT_ID = line.replace('\n', '').replace('spotify_client_id=', '')
                elif(line.startswith('spotify_client_secret=')):
                    spotifyCore.CLIENT_SECRET = line.replace('spotify_client_secret=', '')
                
    except Exception as e:
        print(e)

def save_spotifyToken():
    checkPath()
    # Open File
    with open(FILEPATH_SPOTIFY, 'w') as file:
        # Write Token
        file.writelines('token=' + spotifyCore.AUTH_TOKEN + '\nrefresh_token=' + spotifyCore.AUTH_REFRESH_TOKEN)

def save_settings():
    checkPath()
    # Open File
    with open(FILEPATH_SETTINGS, 'w') as file:
        # Write Settings
        file.writelines('spotify_client_id=' + spotifyCore.CLIENT_ID + '\nspotify_client_secret=' + spotifyCore.CLIENT_SECRET)
