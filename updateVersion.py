import requests, os, zipfile, subprocess

def download_file(url):
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(os.path.dirname(__file__) + '\\songGuesser_new.zip', 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian


username = "lordspiegelei"
# url to request
url = f"https://api.github.com/repos/{username}/songGuesser-py/releases/latest"
# make the request and return the json
repo_info = requests.get(url).json()

print('> Downloading newest version of songGuesser...')

download_file(repo_info['assets'][0]['browser_download_url'])

print('> Unpacking zip...')

# Unpack zip
with open(os.path.dirname(__file__) + '\\songGuesser_new.zip', 'rb') as f:
    packz = zipfile.ZipFile(f)
    for name in packz.namelist():
        if(name != 'updateVersion.py'):
            packz.extract(name, os.path.dirname(__file__))

print('> Removing zip file...')

os.remove(os.path.dirname(__file__) + '\\songGuesser_new.zip')

print('> Update successfully done!')
print('> Restarting songGuesser.py ...')
print(' ')
print('<- - - - ->')
print(' ')

subprocess.Popen(['python', os.path.dirname(__file__) + '\\songGuesser.py'])
quit(0)