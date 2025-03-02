from flask import request
from flask_restful import Resource

from .Models.User import UserModel
from .Models.File import FileModel

from .Utils import Utils

class Sharing(Resource):
    def __init__(self):
        self.__UA = UserModel()
        self.__im = FileModel()

    def post(self):
        if request.endpoint == 'publickey':
            return self.get_user_public_key()
        if request.endpoint == 'share':
            return self.share_file_to_user()
        return None, 204

    def get_user_public_key(self):
        try:
            author_id = Utils.get_input('author_id')
            guest_id = Utils.get_input('guest_id')
            api_token = Utils.get_input('api_token')

            if not self.__UA.check_api_token(author_id, api_token):
                raise Exception('Permission denied: either author_id or api_token is wrong')
    
            elif not self.__UA.check_user_exist(guest_id):
                raise Exception('Guest not found')
            
            else:
                public_key, key_length = self.__UA.get_user_public_key(guest_id)
                return {
                    'error' : False,
                    'public_key' : public_key,
                    'key_length' : key_length
                }, 200

        except Exception as e:
            print(e)
            return {
                'error' : True,
                'message' : str(e)
            }, 400

    def share_file_to_user(self):
        try:
            author_id = Utils.get_input('author_id')
            guest_id = Utils.get_input('guest_id')
            api_token = Utils.get_input('api_token')
            file_id = Utils.get_input('file_id')
            passphrase = Utils.get_input('passphrase')

            if not self.__UA.check_api_token(author_id, api_token):
                raise Exception('Permission denied: either author_id or api_token is wrong')
            
            elif not self.__im.is_author(author_id, file_id):
                raise Exception('Permission denied: this user is not the author')
            
            elif not self.__im.check_file_exist(author_id, file_id):
                raise Exception('file not found')
            
            elif self.__im.check_file_exist(guest_id, file_id):
                raise Exception('Already shared')
            
            elif not self.__UA.check_user_exist(guest_id):
                raise Exception('Guest not found')
            
            else:
                self.__im.share_file_to_user(file_id, guest_id, passphrase)

                return {
                    'error' : False,
                    'message' : 'shared successfully'
                }, 200

        except Exception as e:
            print(e)
            return {
                'error' : True,
                'message' : str(e)
            }, 400
