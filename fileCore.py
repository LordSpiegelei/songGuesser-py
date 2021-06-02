import spotifyCore
import os

FILEPATH_SPOTIFY = os.path.dirname(__file__) + '\\spotifydata.data'

def load_spotifyToken():
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

def save_spotifyToken():
    # Open File
    with open(FILEPATH_SPOTIFY, 'w') as file:
        # Write Token
        file.writelines('token=' + spotifyCore.AUTH_TOKEN + '\nrefresh_token=' + spotifyCore.AUTH_REFRESH_TOKEN)
