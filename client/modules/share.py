from modules.crypt import RSA
from modules.utils import Utils

import requests
import modules.auth as auth

class ShareFile:
    def __init__(self, ip='127.0.0.1', port='5000'):
        self.__ip = ip
        self.__port = port
        self.__default_url = 'http://{0}:{1}'.format(self.__ip, self.__port)

    def getPassphrase(self, api_token, user_id, file_id):
        url = self.__default_url + '/passphrase'
        res = requests.post(url, params={
            'api_token': api_token,
            'user_id': user_id,
            'file_id': file_id
        })
        res = res.json()
        return res

    def getPublicKey(self, guest_id):
        url = self.__default_url + '/publickey'

        response = requests.post(url, params={
            'author_id': auth.user_id,
            'guest_id': guest_id,
            'api_token': auth.api_token
        })
        response = response.json()
        return response
    
    def shareFile(self, api_token, user_id, file_id, guest_id):
        # get user passphrase
        # ppRes: getPassphrase response
        ppRes = self.getPassphrase(auth.api_token, auth.user_id, file_id) 
        
        # decrypt passphrase
        if not ppRes['error']:
            passphrase = ppRes['passphrase']
            key_length = ppRes['key_length']
        
            aes_key = RSA().decrypt(passphrase, auth.private_key, key_length)
        
            # pkRes: getPublicKey response
            pkRes = self.getPublicKey(guest_id)
        
            if not pkRes['error']:
                guest_public_key = pkRes['public_key']
                guest_key_length = pkRes['key_length']
                guest_passphrase = RSA().encrypt(aes_key, guest_public_key, guest_key_length)

                url = self.__default_url + '/share'
                
                shareRes = requests.post(url, params={
                    'author_id': user_id,
                    'api_token': api_token,
                    'file_id': file_id,
                    'guest_id': guest_id,
                    'passphrase': guest_passphrase
                })
                
                shareRes = shareRes.json()
                
                return shareRes['message']
            else:
                return pkRes['message']
        else:
            return ppRes['message']

class ShareFileUI:
    @staticmethod
    def shareFile_UI():
        Utils.clrscr()
        try:
            print('<Share File>\n')
            file_id = input('File ID: ')
            guest_id = input('User ID:  ')
            message = ShareFile(auth.ip, auth.port).shareFile(auth.api_token, auth.user_id, file_id, guest_id)
            print(message)
        except Exception as e:
            print('Error: ' + str(e))
        print('\n')
        Utils.pause()
