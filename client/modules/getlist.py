from modules.utils import Utils
import requests
import modules.auth as auth

class GetFileList:
    def __init__(self, ip='127.0.0.1', port='5000'):
        self.__ip = ip
        self.__port = port
        self.__default_url = 'http://{0}:{1}'.format(self.__ip, self.__port)

    def getFiles(self, user_id, api_token):        
        url = self.__default_url + '/viewall'
        res = requests.post(url, params={
            'user_id': user_id,
            'api_token': api_token
        })
        res = res.json()
        return res

class GetFileListUI:
    @staticmethod
    def GetFileList_UI():
        Utils.clrscr()
        try:
            res = GetFileList(auth.ip, auth.port).getFiles(auth.user_id, auth.api_token)
            if not res['error']:
                numberOfFiles = int(res['total_files'])
                if numberOfFiles == 0:
                    print('Your file list is empty.')
                else:        
                    print('\n\t\t{0}\'s file list:\n'.format(auth.user_name))
                    print('\tFile ID:\t\t File Name:\n')
                    
                    for i in range(numberOfFiles):
                        file_id, file_name = res['file_list'][i]
                        print('\t', file_id, '\t\t\t', file_name)
            else:
                print(res['message'])
        except Exception as e:
            print('Error: ' + str(e))
        print('\n')
        Utils.pause()
