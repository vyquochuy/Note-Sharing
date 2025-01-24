from modules.utils import Utils
from modules.crypt import RSA, AES

import modules.auth as auth
import requests, json, os

class UploadFile:
    def __init__(self, ip='127.0.0.1', port='5000'):
        self.__ip = ip
        self.__port = port
        self.__default_url = 'http://{0}:{1}'.format(self.__ip, self.__port)
        self.__aes = AES()

    def get_public_key(self):
        url = self.__default_url + '/publickey'

        response = requests.post(url, params={
            'author_id': auth.user_id,
            'guest_id': auth.user_id,
            'api_token': auth.api_token
        })

        response = json.loads(response.text)

        if response["error"]:
            raise Exception(response["error"])
        else:
            return response["public_key"], response["key_length"]

    def upload_file(self, file_path):
        url = self.__default_url + '/upload'
        
        public_key, key_length = self.get_public_key()

        try:
            encrypted_file, real_name, key, original_checksum = self.__aes.encrypt(file_path)
            if not all([encrypted_file, real_name, key, original_checksum]):
                raise ValueError("Encryption failed, returned None values")
        except Exception as e:
            raise Exception(f"Encryption error: {str(e)}")

        key = RSA.encrypt(key, public_key, key_length)
        checksum = RSA.encrypt(original_checksum, public_key, key_length)

        with open(encrypted_file, 'rb') as f:
            files = [('file', (encrypted_file, f, 'application/octet-stream'))]

            response = requests.post(url, params={
                'user_id': auth.user_id,
                'api_token': auth.api_token,
                'passphrase': key,
                'real_name': real_name,
                'checksum': checksum
            }, files=files)

        response = json.loads(response.text)

        if response["error"]:
            raise Exception(response["message"])
        else:
            # Delete temp files after successful upload
            os.remove(encrypted_file)
            return response["message"]

class UploadUI:
    @staticmethod
    def main():
        Utils.clrscr()
        print('Upload a new file to server!')
        try:
           file_path = input("Path to the file: ")
           upload_status = UploadFile().upload_file(file_path)
        except Exception as e:
            print('Error: ' + str(e))
        else:
            print(upload_status)
            
        Utils.pause()
