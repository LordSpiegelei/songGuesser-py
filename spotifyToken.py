import requests
import base64
import webbrowser
import spotifyCore
import fileCore


AUTH_URL = 'https://accounts.spotify.com/api/token'

SCOPES = 'user-read-private%20user-read-email%20user-read-currently-playing%20user-read-playback-state'
REDIRECT_URI = 'http://localhost:187'

def token_request():
    global AUTH_URL
    global REDIRECT_URI
    global SCOPES
    print('> Opening authorize website...')

    # Open new window with Auth
    webbrowser.open('https://accounts.spotify.com/authorize?response_type=code&client_id=' + spotifyCore.CLIENT_ID + '&scope=' + SCOPES + '&redirect_uri=' + REDIRECT_URI, new=1)

    # Get new url
    codeUrl = input('> Enter loaded Website Url: ')

    # Replace redirect url to get code
    AUTH_CODE = codeUrl.replace(REDIRECT_URI + '/?code=', '')

    # Get the token
    # POST
    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'authorization_code',
        'client_id': spotifyCore.CLIENT_ID,
        'client_secret': spotifyCore.CLIENT_SECRET,
        'code': AUTH_CODE,
        'redirect_uri': REDIRECT_URI,
    })

    # convert the response to JSON
    auth_response_data = auth_response.json()

    # save the access token
    spotifyCore.AUTH_TOKEN = auth_response_data['access_token']
    spotifyCore.AUTH_REFRESH_TOKEN = auth_response_data['refresh_token']

    # Save token to file
    fileCore.save_spotifyToken()

    print('> Successfully requested new Spotify Token')


def token_refresh():
    global AUTH_URL
    global REDIRECT_URI

    data = spotifyCore.CLIENT_ID + ":" + spotifyCore.CLIENT_SECRET

    # Standard Base64 Encoding
    encodedBytes = base64.b64encode(data.encode("utf-8"))
    encodedStr = str(encodedBytes, "utf-8")


    requestHeaders = {
            'Authorization': 'Basic {token}'.format(token=encodedStr)
        }

    # Send POST
    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'refresh_token',
        'refresh_token': spotifyCore.AUTH_REFRESH_TOKEN,
    }, headers=requestHeaders)

    # convert the response to JSON
    auth_response_data = auth_response.json()

    # save the access token
    spotifyCore.AUTH_TOKEN = auth_response_data['access_token']

    # Save token to file
    fileCore.save_spotifyToken()
