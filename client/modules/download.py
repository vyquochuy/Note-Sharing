from modules.getlist import GetFileList
from modules.crypt import RSA, AES
from modules.utils import Utils

import requests, os, shutil
import modules.auth as auth

class Download:
    def __init__(self, ip='127.0.0.1', port='5000'):
        self.__ip = ip
        self.__port = port
        self.__default_url = 'http://{0}:{1}'.format(self.__ip, self.__port)

    def get_passphrase(self, api_token, user_id, file_id):
        url = self.__default_url + '/passphrase'
        res = requests.post(url, params={
            'api_token': api_token,
            'user_id': user_id,
            'file_id': file_id
        })
        res = res.json()
        return res

    def get_checksum(self, user_id, file_id, api_token):
        url = self.__default_url + '/checksum'

        res = requests.post(url, params={
            'api_token': api_token,
            'user_id': user_id,
            'file_id': file_id
        })

        res = res.json()
        return res

    def fileDownload(self, user_id, file_id, api_token):
        url = self.__default_url + '/download'
        res = requests.post(url, params={
            'user_id': user_id,
            'file_id': file_id,
            'api_token': api_token
        }, stream=True)
        # Create a directory to save
        save_dir = 'downloads'

        if not os.path.isdir(save_dir):
            os.mkdir(save_dir)

        ppRes = self.get_passphrase(api_token, user_id, file_id)  # ppRes: get_passphrase response
        ckRes = self.get_checksum(user_id, file_id, api_token)  # ckRes: get_checksum response

        if not ppRes['error'] and not ckRes['error']:
            # For file decryption
            filename = ppRes['real_name']
            passphrase = ppRes['passphrase']
            key_length = ppRes['key_length']

            # For file checksum
            original_checksum = ckRes['checksum']
            author_public_key = ckRes['author_public_key']
            author_key_length = ckRes['author_key_length']

            aesKey = RSA().decrypt(passphrase, auth.private_key, key_length)

            if res.status_code == 200:
                with open('{0}/{1}_{2}'.format(save_dir, file_id, filename), 'wb') as f:
                    res.raw.decode_content = True

                    shutil.copyfileobj(res.raw, f)

                    encryptedFile = '{0}/{1}_{2}'.format(save_dir, file_id, filename)

                    checksum = AES().decrypt(encryptedFile, encryptedFile, aesKey)

                    encrypted_checksum = RSA().encrypt(checksum, author_public_key, author_key_length)

                if encrypted_checksum == original_checksum:
                    print('File {0} downloaded successfully, with correct author checksum'.format(filename))
                else:
                    print('File {0} downloaded successfully, but corrupted due to an unknown reason.'.format(filename))
            else:
                res = res.json()
                print(res['message'])
        else:
            if ppRes['error']:
                print(ppRes['message'])
            if ckRes['error']:
                print(ckRes['message'])

class DownloadUI:
    @staticmethod
    def downloadFile_UI():
        Utils.clrscr()
        try:
            print('<Download File>\n')
            print('\t1. Download single file')
            print('\t2. Download all files\n')

            ans = int(input('What\'s your choice then? '))
            Utils.clrscr()
            if ans == 1:
                print('<Download single file>\n')
                file_id = input('File ID: ')
                Download(auth.ip, auth.port).fileDownload(auth.user_id, file_id, auth.api_token)

            elif ans == 2:
                res = GetFileList(auth.ip, auth.port).getFiles(auth.user_id, auth.api_token)
                if not res['error']:
                    numberOfFiles = int(res['total_files'])
                    if numberOfFiles == 0:
                        print('Your file list is empty.')
                    else:
                        for i in range(numberOfFiles):
                            file_id, __ = res['file_list'][i]
                            Download(auth.ip, auth.port).fileDownload(auth.user_id, file_id, auth.api_token)
                        print('Downloaded all files in your file list successfully!')
                else:
                    print(res['message'])
            else:
                raise Exception('Invalid choice.')
        except Exception as e:
            print('Error: ' + str(e))

        Utils.pause()
