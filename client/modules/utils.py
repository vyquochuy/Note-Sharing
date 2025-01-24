from PIL import Image
import os
import shutil

class Utils:
    @staticmethod
    def clrscr():
        '''Clear the screen
        '''
        os.system('clear') if os.name == 'posix' else os.system('cls')
    
    @staticmethod
    def pause():
        '''Pause the screen before clearing
        '''
        input('Press any key to continue...')
    
    @staticmethod
    def convert_to_encryptable(file_path):
        '''Convert any file to an encryptable type if needed.

        Input:
            - file_path: path to the file
        
        Output:
            - converted file path, original file name
        '''
        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension in ['.jpg', '.jpeg', '.bmp', '.tiff']:
            encryptable_type = '{0}.png'
            filename = os.path.basename(file_path).split('.')[0]
            new_filename = encryptable_type.format(filename)
            with Image.open(file_path) as img:
                img.save(new_filename)
            return new_filename, os.path.basename(file_path)
        else:
            temp_file = 'temp_' + os.path.basename(file_path)
            shutil.copy(file_path, temp_file)
            return temp_file, os.path.basename(file_path)
