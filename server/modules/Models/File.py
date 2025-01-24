from flask import current_app
from ..db import get_db

import os

class FileModel:
    def __init__(self):
        self.__db = get_db()

    def create_absolute_file_name(self, file):
        '''Create an absolute name for file.

        Input:
            - file : uploaded file
        
        Output:
            - new_filename : new file name (to store on server)
            - new_file_id : new ID
        '''
        filename = file.filename.split('.')[0]

        new_file_id = str(self.get_total_files() + 1)
        _, extension = os.path.splitext(file.filename.lower())
        new_filename = f'{new_file_id}{extension}'

        return new_filename, new_file_id

    def save_file_dir(self, file):
        '''Save file to directory (default in UPLOAD_FOLDER)

        Input:
            - file : file to save
        
        Output:
            - new_name : file name on server
            - new_file_id : file id
        '''
        new_name, new_file_id = self.create_absolute_file_name(file)
        upload_folder = os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'])
        
        if not os.path.isdir(upload_folder):
            os.mkdir(upload_folder)

        new_path = os.path.join(upload_folder, new_name)
        file.save(new_path)

        return new_name, new_file_id

    def save_file_record(self, user_id, file_id, passphrase, location, real_name, checksum):
        '''Adding records to file database.

        Input:
            - user_id
            - file_id
            - passphrase : Encrypted with RSA
            - location : Filename stored on server.
            - real_name : Original filename when uploaded.
            - checksum : Checksum
        '''
        # Add records to file database
        self.__db.execute(
            'INSERT INTO files (id, author_id, location, real_name, checksum) VALUES (?, ?, ?, ?, ?)',
            (file_id, user_id, location, real_name, checksum)
        )

        self.__db.commit()

        self.share_file_to_user(file_id, user_id, passphrase)

    def share_file_to_user(self, file_id, user_id, passphrase):
        '''Adding records to share to other user.

        Input:
            - file_id
            - user_id : ID to share
            - passphrase : new passphrase (Encrypted with RSA)
        '''
        self.__db.execute(
            'INSERT INTO sharing (file_id, user_id, passphrase) VALUES (?, ?, ?)',
            (file_id, user_id, passphrase)
        )

        self.__db.commit()

    def get_total_files(self):
        '''Count total files on server.

        Output:
            - total_files
        '''
        db_exec = self.__db.execute(
            'SELECT COUNT(*) FROM files', ())
        
        row = db_exec.fetchone()
        return row[0]
    
    def get_files_of_user(self, user_id):
        '''Get files of user.

        Input:
            - user_id

        Output:
            - Many rows, each row has this format:
                - file_id : ID of the file on server.
                - file_real_name : Original filename
        '''
        db_exec = self.__db.execute(
            'SELECT files.id, files.real_name FROM files, sharing WHERE files.id = sharing.file_id AND sharing.user_id = ?',
            (user_id,)
        )

        rows = db_exec.fetchall()

        return rows

    def get_file_passphrase(self, user_id, file_id):
        '''Get file passphrase (for AES decryption)

        Input:
            - user_id : ID of the user who can download file_id
            - file_id : ID of the file.

        Output:
            - passphrase : File passphrase to decrypt.
        '''
        db_exec = self.__db.execute(
            'SELECT passphrase FROM sharing WHERE user_id = ? AND file_id = ?',
            (user_id, file_id)
        )

        row = db_exec.fetchone()

        return row[0]
    
    def get_file_checksum(self, file_id):
        '''Get file checksum info

        Input:
            - file_id : ID of the file

        Output:
            - author_id : Author ID
            - file_checksum : File checksum
        '''

        db_exec = self.__db.execute(
            'SELECT author_id, checksum FROM files WHERE id = ?',
            (file_id,)
        )

        row = db_exec.fetchone()

        return row[0], row[1]

    def check_file_exist(self, user_id, file_id):
        '''Check if file_id exist (aka user_id has permissions with it).

        Input:
            - user_id : ID of user
            - file_id : ID of file
        
        Return:
            - True if user has the right with it, False otherwise.
        '''
        db_exec = self.__db.execute(
            'SELECT COUNT(*) FROM sharing WHERE user_id = ? AND file_id = ?',
            (user_id, file_id)
        )

        row = db_exec.fetchone()

        return row[0] != 0
    
    def get_file_filename(self, user_id, file_id):
        '''Get file filename (for download)

        Input:
            - user_id : User ID (has permissions)
            - file_id : File ID

        Return:
            - file_location : Filename on server
            - file_realname : Original file name
        '''
        db_exec = self.__db.execute(
            'SELECT files.location, files.real_name FROM files, sharing WHERE sharing.user_id = ? AND sharing.file_id = ? AND sharing.file_id = files.id',
            (user_id, file_id)
        )

        row = db_exec.fetchone()

        return row[0], row[1]
    
    def is_author(self, user_id, file_id):
        '''Check if user is author (the-one-who-uploaded) of the file.

        Input:
            - user_id : ID of the author (to check)
            - file_id : ID of the file

        Return:
            - True if user is the author, False otherwise
        '''
        db_exec = self.__db.execute(
            'SELECT COUNT(*) FROM files WHERE id = ? AND author_id = ?',
            (file_id, user_id)
        )

        row = db_exec.fetchone()
        
        return row[0] == 1
