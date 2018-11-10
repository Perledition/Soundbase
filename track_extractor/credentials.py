import sys

usernameStr = ''
passwordStr = ''

def serve_credentials(return_value):

        if return_value == 'user':
            if usernameStr == '':
                print('Bitte Username in credentials.py eintragen')
                sys.exit()
            return usernameStr
        else:
            if passwordStr == '':
                print('Bitte Passwort in credentials.py eintragen')
                sys.exit()
            return passwordStr
