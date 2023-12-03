from cryptography.fernet import Fernet
from tempfile import mkdtemp, mkstemp
import subprocess
import unittest
import shutil
import sys
import os


class TestRecrypt(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file1_content = str.encode('I hope you have a nice day')
        self.file2_content = str.encode('I hope you have a nice day too')

        self.key = Fernet.generate_key()
        self.key_str = self.key.decode('utf-8')
        self.fernet = Fernet(self.key)

        self.file1_content_encrypted = self.fernet.encrypt(self.file1_content)
        self.file2_content_encrypted = self.fernet.encrypt(self.file2_content)

        self.python_executable = sys.executable
        self.recrypt_script = os.path.join(os.getcwd(), 'recrypt.py')
    
    def call_recrypt(self, action, input_path, output_path=None, key=None,
                     password=None, overwrite=False):
        args = [
            self.python_executable,
            self.recrypt_script,
            f'--{action}',
            input_path,
        ]

        if output_path:
            args.extend(['--output', output_path])
        if key:
            args.extend(['--key', key])
        if password:
            args.extend(['--password', password])
        if overwrite:
            args.append('--overwrite')
        
        subprocess.call(args)
        
    def create_temp_file(self, filename, content, directory=None):
        file_handle, file_path = mkstemp(dir=directory)

        file_descriptor = os.fdopen(file_handle, 'wb')
        file_descriptor.write(content)
        file_descriptor.close()

        return file_path

    def setUp(self):
        self.dir1 = mkdtemp()
        self.dir2 = mkdtemp(dir=self.dir1)

        self.file1 = self.create_temp_file('file1', self.file1_content, directory=self.dir1)
        self.file2 = self.create_temp_file('file2', self.file2_content, directory=self.dir2)
    
    def tearDown(self):
        shutil.rmtree(self.dir1)
    
    def test_overwriting(self):
        self.call_recrypt('encrypt', self.dir1, overwrite=True, key=self.key_str)
        
        with open(self.file1, 'rb') as rf:
            self.assertEqual(rf.read(), self.file1_content_encrypted)
        with open(self.file2, 'rb') as rf:
            self.assertEqual(rf.read(), self.file2_content_encrypted)
        
        self.call_recrypt('decrypt', self.dir1, overwrite=True, key=self.key_str)

        with open(self.file1, 'rb') as rf:
            self.assertEqual(rf.read(), self.file1_content)
        with open(self.file2, 'rb') as rf:
            self.assertEqual(rf.read(), self.file2_content)

if __name__ == '__main__':
    unittest.main()