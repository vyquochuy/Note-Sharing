from modules.auth import AuthenticationUI
from modules.upload import UploadUI
from modules.getlist import GetFileListUI
from modules.download import DownloadUI
from modules.share import ShareFileUI
from modules.utils import Utils

import modules.auth as auth
import requests, json

def try_connect(ip, port):
    '''Try connecting to the server.

    Input:
        - ip (str) : Server IP
        - port (str) : Port to connect
    
    Output:
        - True if connectable, False otherwise.
    '''
    try:
        url = 'http://{0}:{1}/ping'.format(ip, port)
        res = requests.get(url)

        res = json.loads(res.text)

        if res["ping"] == "pong":
            return True
    except Exception as e:
        print(str(e))
        return False

def main(): 
    auth.ip = input('Server IP: ')
    auth.port = input('Port: ')

    if not try_connect(auth.ip, auth.port):
        print('Cannot connect to server. Check your connection and try again.')
        exit(0)

    while 1:
        if not auth.logged_in:
            AuthenticationUI.Menu_UI()
        else:
            # This should be placed inside a class named MainUI
            Utils.clrscr()
            print('Hello {0}'.format(auth.user_name))
            print('Your current choice is: ')
            print('\t1. Log out')
            print('\t2. Upload a new file to server')
            print('\t3. Get file list from server')
            print('\t4. Download file from server')
            print('\t5. Share file with another user')
            try:
                ans = int(input('Your choice: '))

                if ans == 1:
                    AuthenticationUI.Logout_UI()
                elif ans == 2:
                    UploadUI.main()                    
                elif ans == 3:
                    GetFileListUI.GetFileList_UI()                    
                elif ans == 4:
                    DownloadUI.downloadFile_UI()
                elif ans == 5:
                    ShareFileUI.shareFile_UI()
                else:
                    raise Exception('Invalid choice')
            except Exception as e:
                print('Error: ' + str(e))
                Utils.pause()

if __name__ == '__main__':
    main()
