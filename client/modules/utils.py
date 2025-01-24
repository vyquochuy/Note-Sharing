import os

class Utils:
    @staticmethod
    def clrscr():
        '''Clear the screen'''
        os.system('clear') if os.name == 'posix' else os.system('cls')
    
    @staticmethod
    def pause():
        '''Pause the screen before clearing'''
        input('Press any key to continue...')
    
    @staticmethod
    def convert_to_encryptable(file_path):
        '''Prepare any file for encryption by verifying its existence.
        
        Input:
            - file_path: Path to the file.

        Output:
            - file_path: Path to the original file (unchanged).
            - original_file_name: Original file name.
        '''
        # Kiểm tra xem tệp có tồn tại không
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Lấy tên tệp gốc
        original_file_name = os.path.basename(file_path)
        
        # Trả về đường dẫn tệp và tên gốc của tệp
        return file_path, original_file_name
