from flask import request
from flask_restful import Resource, reqparse

from .Models.User import UserModel
from .Models.File import FileModel

from .Utils import Utils
import os

class UploadFiles(Resource):
    def __init__(self):
        self.__UA = UserModel()
        self.__im = FileModel()
        self.ALLOWED_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.bmp', '.txt', '.pdf', '.docx', '.xlsx', '.zip', '.rar']

    def get_file(self):
        try:
            _file = request.files['file']

        except Exception:
            raise Exception('No file selected')
        else:
            _, extension = os.path.splitext(_file.filename.lower())

            if extension not in self.ALLOWED_EXTENSIONS:
                raise Exception('Extension not allowed')

            else:
                return _file

    def post(self):
        try:
            user_id = Utils.get_input('user_id')
            api_token = Utils.get_input('api_token')
            passphrase = Utils.get_input('passphrase')
            real_name = Utils.get_input('real_name')
            checksum = Utils.get_input('checksum')

            image = self.get_file()
           
            if not self.__UA.check_api_token(user_id, api_token):
                raise Exception('Permission denied: either user_id or api_token is wrong')
            
            else:
                new_path, new_file_id = self.__im.save_file_dir(image)
                self.__im.save_file_record(
                    user_id, new_file_id,
                    passphrase, new_path,
                    real_name, checksum
                )

        except Exception as e:
            print(e)
            return {
                'error' : True,
                'message' : str(e)
            }, 400
        else:
            return {
                'error' : False,
                '_filename' : real_name,
                'file_id' : new_file_id,
                'message' : 'upload successful'
            }, 200
