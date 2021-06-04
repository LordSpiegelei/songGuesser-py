import requests
import spotifyToken

CLIENT_ID = None
CLIENT_SECRET = None

AUTH_TOKEN = None
AUTH_REFRESH_TOKEN = None

temp_userInfo = None

# base URL of all Spotify API endpoints
BASE_URL = 'https://api.spotify.com/v1/'

def get_userInfo(getNewData):
    global temp_userInfo
    global BASE_URL
    global AUTH_TOKEN
    global AUTH_REFRESH_TOKEN

    # Check if temp_userInfo is set
    if((temp_userInfo == None) or (getNewData == True)):
        # Update temp_userInfo

        # Set request headers
        requestHeaders = {
            'Authorization': 'Bearer {token}'.format(token=AUTH_TOKEN)
        }

        # Pull /me info
        responseObj = requests.get(BASE_URL + 'me', 
                        headers=requestHeaders)

        # Check if request was successful
        responseCode = responseObj.status_code

        if(responseCode == 403):
            print('Spotify error 403 on UserInfo request...')
            print(responseObj.json())
            return None
        elif(responseCode == 401):
            print(responseObj)
            print('> Refreshing Spotify Token...')
            if(AUTH_REFRESH_TOKEN == None):
                spotifyToken.token_request()
                return get_userInfo(getNewData)
            else:
                spotifyToken.token_refresh()
                return get_userInfo(getNewData)
        elif(responseCode == 200):
            print("> Success")
            # Set temp_userInfo
            temp_userInfo = responseObj.json()
            return responseObj.json()
        else:
            print('> Spotif error ' + responseCode + " on UserInfo request...")
            print(responseObj.json())
            return None
    
    else:
        # return temp_userInfo
        return temp_userInfo

def player_currentSong():
    global AUTH_TOKEN
    global AUTH_REFRESH_TOKEN
    # Update temp_userInfo

    # Set request headers
    requestHeaders = {
        'Authorization': 'Bearer {token}'.format(token=AUTH_TOKEN)
    }

    # Pull /me info
    responseObj = requests.get('https://api.spotify.com/v1/me/player/currently-playing', 
                    headers=requestHeaders)

    # Check if request was successful
    responseCode = responseObj.status_code

    if(responseCode == 403):
        print('Spotify error 403 on CurrentSong request...')
        print(responseObj.json())
        return None
    elif(responseCode == 401):
        if(AUTH_REFRESH_TOKEN == None):
            spotifyToken.token_request()
            return player_currentSong()
        else:
            spotifyToken.token_refresh()
            return player_currentSong()
    elif(responseCode == 200):
        return responseObj.json()
    else:
        print('> Spotif error ' + str(responseCode) + " on CurrentSonng request...")
        print(responseObj.json())
        return None

def player_pausePlayback():
    global AUTH_TOKEN
    global AUTH_REFRESH_TOKEN
    # Update temp_userInfo

    # Set request headers
    requestHeaders = {
        'Authorization': 'Bearer {token}'.format(token=AUTH_TOKEN)
    }

    # Pull /me info
    responseObj = requests.put('https://api.spotify.com/v1/me/player/pause', 
                    headers=requestHeaders)

    # Check if request was successful
    responseCode = responseObj.status_code

    if(responseCode == 403):
        print('Spotify error 403 on PausePlayback request...')
        print(responseObj.json())
        return False
    elif(responseCode == 401):
        if(AUTH_REFRESH_TOKEN == None):
            spotifyToken.token_request()
            player_pausePlayback()
        else:
            spotifyToken.token_refresh()
            player_pausePlayback()
    elif(responseCode == 204):
        return True
    else:
        print('> Spotif error ' + str(responseCode) + " on PausePlayback request...")
        print(responseObj.json())
        return False

def player_resumePlayback():
    global AUTH_TOKEN
    global AUTH_REFRESH_TOKEN
    # Update temp_userInfo

    # Set request headers
    requestHeaders = {
        'Authorization': 'Bearer {token}'.format(token=AUTH_TOKEN)
    }

    # Pull /me info
    responseObj = requests.put('https://api.spotify.com/v1/me/player/play', 
                    headers=requestHeaders)

    # Check if request was successful
    responseCode = responseObj.status_code

    if(responseCode == 403):
        print('Spotify error 403 on ResumePlayback request...')
        print(responseObj.json())
        return False
    elif(responseCode == 401):
        if(AUTH_REFRESH_TOKEN == None):
            spotifyToken.token_request()
            player_resumePlayback()
        else:
            spotifyToken.token_refresh()
            player_resumePlayback()
    elif(responseCode == 204):
        return True
    else:
        print('> Spotif error ' + str(responseCode) + " on ResumePlayback request...")
        print(responseObj.json())
        return False

def player_skipPlayback():
    global AUTH_TOKEN
    global AUTH_REFRESH_TOKEN
    # Update temp_userInfo

    # Set request headers
    requestHeaders = {
        'Authorization': 'Bearer {token}'.format(token=AUTH_TOKEN)
    }

    # Pull /me info
    responseObj = requests.post('https://api.spotify.com/v1/me/player/next', 
                    headers=requestHeaders)

    # Check if request was successful
    responseCode = responseObj.status_code

    if(responseCode == 403):
        print('Spotify error 403 on SkipPlayback request...')
        print(responseObj.json())
        return False
    elif(responseCode == 401):
        if(AUTH_REFRESH_TOKEN == None):
            spotifyToken.token_request()
            player_skipPlayback()
        else:
            spotifyToken.token_refresh()
            player_skipPlayback()
    elif(responseCode == 204):
        return True
    else:
        print('> Spotif error ' + str(responseCode) + " on SkipPlayback request...")
        print(responseObj.json())
        return False

def player_seekPosition(position_ms):
    global AUTH_TOKEN
    global AUTH_REFRESH_TOKEN
    # Update temp_userInfo

    # Set request headers
    requestHeaders = {
        'Authorization': 'Bearer {token}'.format(token=AUTH_TOKEN)
    }

    # Pull /me info
    responseObj = requests.put('https://api.spotify.com/v1/me/player/seek', params={'position_ms': int(position_ms)},
                    headers=requestHeaders)

    # Check if request was successful
    responseCode = responseObj.status_code

    if(responseCode == 403):
        print('Spotify error 403 on SeekPlayback request...')
        print(responseObj.json())
        return False
    elif(responseCode == 401):
        if(AUTH_REFRESH_TOKEN == None):
            spotifyToken.token_request()
            player_seekPosition(position_ms)
        else:
            spotifyToken.token_refresh()
            player_seekPosition(position_ms)
    elif(responseCode == 204):
        return True
    else:
        print('> Spotif error ' + str(responseCode) + " on SeekPlayback request...")
        print(responseObj.json())
        return False


# # save the access token
# access_token = auth_response_data['access_token']


# headers = {
#     'Authorization': 'Bearer {token}'.format(token=access_token)
# }

# # pull all artists albums
# r = requests.get(BASE_URL + 'me', 
#                  headers=headers)
#                  #params={'include_groups': 'album', 'limit': 50})
# d = r.json()

# print(d)