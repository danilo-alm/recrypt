from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
from operation import Operation
import base64
import sys
import os


class CryptoHandler:
    def __init__(self, operation, password):
        if not isinstance(operation, Operation):
            sys.exit('operation must be of type Operation')
        
        self.key = self.__generate_key_from_password(password)
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

    def __handle_file(self, file_path, output_path):
        with open(file_path, 'rb') as rf:
            data = rf.read()

        if self.operation == Operation.ENCRYPT:
            data = self.fernet.encrypt(data)
        else:
            data = self.fernet.decrypt(data)

        with open(output_path, 'wb') as wf:
            wf.write(data)

    def __handle_directory(self, directory_path, output_path):
        if os.path.exists(output_path):
            output_path = os.path.join(output_path, os.path.basename(directory_path))
         
        try:
            os.mkdir(output_path)
        except FileExistsError:
            sys.exit(f'Output directory "{output_path}" already exists.')

        for entry in os.scandir(directory_path):
            output_path = entry.path if os.path.samefile(directory_path, output_path) \
                else os.path.join(output_path, entry.name)
            if entry.is_dir():
                self.handle_directory(
                    directory_path=entry.path,
                    output_path=os.path.join(after_operation_dir_path, entry.name),
                )
            elif entry.is_file():  # entry can also be symlink
                self.__handle_file(
                    filepath=entry.path,
                    output_path=output_path
                )
