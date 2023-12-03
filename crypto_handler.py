from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
from operation import Operation
import base64
import sys
import os


class CryptoHandler:
    def __init__(self, operation, password=None, key=None):
        if not isinstance(operation, Operation):
            sys.exit('operation must be of type Operation')
        
        if not (password or key):
            sys.exit('Either password or key must be provided')
        
        self.key = str.encode(key) or self.__generate_key_from_password(password)
        self.fernet = Fernet(self.key)
        self.operation = operation

    def __generate_key_from_password(self, password):
        password_bytes = str.encode(password)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            salt=str.encode(''),
            length=32,
            iterations=480000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password_bytes))

    def __handle_file(self, input_path, output_path):
        with open(input_path, 'rb') as rf:
            data = rf.read()

        if self.operation == Operation.ENCRYPT:
            data = self.fernet.encrypt(data)
        else:
            data = self.fernet.decrypt(data)

        with open(output_path, 'wb') as wf:
            wf.write(data)

    def __handle_directory(self, input_path, output_path):
        if os.path.exists(output_path):
            output_path = os.path.join(output_path, os.path.basename(directory_path))
         
        try:
            os.mkdir(output_path)
        except FileExistsError:
            sys.exit(f'Output directory "{output_path}" already exists.')

        for entry in os.scandir(input_path):
            output_path = entry.path if os.path.samefile(input_path, output_path) \
                else os.path.join(output_path, entry.name)
            if entry.is_dir():
                self.handle_directory(
                    input_path=entry.path,
                    output_path=os.path.join(output_path, entry.name),
                )
            elif entry.is_file():  # entry can also be symlink
                self.__handle_file(
                    filepath=entry.path,
                    output_path=output_path
                )
    
    def __handle_path(self, input_path, output_path):
        if os.path.isdir(input_path):
            self.__handle_directory(input_path, output_path)
        elif os.path.isfile(input_path):
            self.__handle_file(input_path, output_path)
        else:
            sys.exit(f'Path "{input_path}" does not exist.')

    def encrypt(self, input_path, output_path):
        if self.operation != Operation.ENCRYPT:
            sys.exit('Cannot encrypt with decrypt operation')
        self.__handle_path(input_path, output_path)

    def decrypt(self, input_path, output_path):
        if self.operation != Operation.DECRYPT:
            sys.exit('Cannot decrypt with encrypt operation')
        self.__handle_path(input_path, output_path)
