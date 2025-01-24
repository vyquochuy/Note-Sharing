from flask import request, send_from_directory, current_app
from flask_restful import Resource

from .Models.File import FileModel
from .Models.User import UserModel

from .Utils import Utils
import os

class DownloadFiles(Resource):
    def __init__(self):
        self.__UA = UserModel()
        self.__im = FileModel()

    def post(self):
        if request.endpoint == 'viewall':
            return self.user_files()
        if request.endpoint == 'passphrase':
            return self.file_passphrase()
        if request.endpoint == 'checksum':
            return self.file_checksum()
        if request.endpoint == 'download':
            return self.download_file()
        return None, 204

    def user_files(self):
        try:
            user_id = Utils.get_input('user_id')
            api_token = Utils.get_input('api_token')

            if not self.__UA.check_api_token(user_id, api_token):
                raise Exception('Permission denied: either user_id or api_token is wrong')
            
            else:
                file_list = []
                for row in self.__im.get_files_of_user(user_id):
                    file_list.append((row[0], row[1]))
        except Exception as e:
            print(e)
            return {
                'error' : True,
                'message' : str(e)
            }, 400
        else:
            return {
                'error' : False,
                'total_files' : len(file_list),
                'file_list' : file_list,
                'message' : 'request successful'
            }, 200

    def file_passphrase(self):
        try:
            api_token = Utils.get_input('api_token')
            file_id = Utils.get_input('file_id')
            user_id = Utils.get_input('user_id')

            if not self.__UA.check_api_token(user_id, api_token):
                raise Exception('Permission denied: either user_id or api_token is wrong')

            elif not self.__im.check_file_exist(user_id, file_id):
                raise Exception('file not found 1')
            
            else:
                passphrase = self.__im.get_file_passphrase(user_id, file_id)
                _, real_name = self.__im.get_file_filename(user_id, file_id)
                _, key_length = self.__UA.get_user_public_key(user_id)

                return {
                    'error' : False,
                    'passphrase' : passphrase,
                    'real_name' : real_name,
                    'key_length' : key_length
                }, 200

        except Exception as e:
            print(e)
            return {
                'error' : True,
                'message' : str(e)
            }, 400
    
    def file_checksum(self):
        try:
            api_token = Utils.get_input('api_token')
            file_id = Utils.get_input('file_id')
            user_id = Utils.get_input('user_id')

            if not self.__UA.check_api_token(user_id, api_token):
                raise Exception('Permission denied: either user_id or api_token is wrong')

            elif not self.__im.check_file_exist(user_id, file_id):
                raise Exception('file not found 2')

            else:
                author_id, checksum = self.__im.get_file_checksum(file_id)
                author_public_key, key_length = self.__UA.get_user_public_key(author_id)

                return {
                    'error' : False,
                    'checksum' : checksum,
                    'author_public_key' : author_public_key,
                    'author_key_length' : key_length
                }
            
        except Exception as e:
            print(e)
            return {
                'error' : True,
                'message' : str(e)
            }, 400 

    def download_file(self):
        try:
            api_token = Utils.get_input('api_token')
            file_id = Utils.get_input('file_id')
            user_id = Utils.get_input('user_id')

            if not self.__UA.check_api_token(user_id, api_token):
                raise Exception('Permission denied: either user_id or api_token is wrong')
                
            elif not self.__im.check_file_exist(user_id, file_id):
                raise Exception('file not found 3')

            else:
                filename, _ = self.__im.get_file_filename(user_id, file_id)

                return send_from_directory(
                    directory = os.path.join(
                        current_app.root_path,
                        current_app.config['UPLOAD_FOLDER']
                        ),
                    path = filename,
                    as_attachment = True
                )
        except Exception as e:
            print(e)
            return {
                'error' : True,
                'message' : str(e)
            }, 400
