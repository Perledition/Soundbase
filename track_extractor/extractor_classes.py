from robobrowser import RoboBrowser
import requests
import re

br = RoboBrowser()
br.open('https://soundcloud.com/connect?client_id=0ZgkqLom8d5E0yJP57kNqk9TRpMmaDwe&display=popup&redirect_uri=http%3A%2F%2Fthehusk.ca%2Fscredirect.asp&response_type=code_and_token&scope=non-expiring&state=SoundCloud_Dialog_7c5ba')


form = br.get_form(id='oauth2-login-form')
form['username'] = 'track_base'
form['password'] = 'PhiMa#SC#44793'
br.submit_form(form)

br.open('http://thehusk.ca/')
src = br.parsed()
print(src)
print('Success')


url = 'http://google.com/favicon.ico'



def is_downloadable(url):
    """
    Does the url contain a downloadable resource
    """
    h = requests.head(url, allow_redirects=True)
    header = h.headers
    content_type = header.get('content-type')
    if 'text' in content_type.lower():
        return False
    if 'html' in content_type.lower():
        return False
    return True


def check_filesize(url):

    h = requests.head(url, allow_redirects=True)
    header = h.headers
    content_length = header.get('content-length', None)
    if content_length and content_length > 2e8:  # 200 mb approx
        return False


def get_filename_from_cd(url):
    """
    Get filename from content-disposition
    """
    r = requests.get(url, allow_redirects=True)
    cd = r.headers.get('content-disposition')
    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname[0]



filename = get_filename_from_cd(url)
open(filename, 'wb').write(r.content)


print is_downloadable('https://www.youtube.com/watch?v=9bZkp7q19f0')
# >> False
print is_downloadable('http://google.com/favicon.ico')
# >> True
