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

        self.password = str.encode('my_secure_password')
        self.key = Fernet.generate_key()

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
    
    def print_file_contents(self, text):
        print(text.center(80, '-'))
        with open(self.file1, 'rb') as rf:
            print(f'File 1: {rf.read()}')
        with open(self.file2, 'rb') as rf:
            print(f'File 2: {rf.read()}\n')
    
    def make_assertions(self,
                       action,
                       file1_path=None,
                       file2_path=None,
                       file1_expected_content=None,
                       file2_expected_content=None):
        if not (file1_path or file2_path):
            file1_path = self.file1
            file2_path = self.file2

        if not (file1_expected_content or file2_expected_content):
            file1_expected_content = self.file1_content
            file2_expected_content = self.file2_content

        if action == 'equal':
            with open(file1_path, 'rb') as rf:
                self.assertEqual(rf.read(), file1_expected_content)
            with open(file2_path, 'rb') as rf:
                self.assertEqual(rf.read(), file2_expected_content)
        elif action == 'not_equal':
            with open(file1_path, 'rb') as rf:
                self.assertNotEqual(rf.read(), file1_expected_content)
            with open(file2_path, 'rb') as rf:
                self.assertNotEqual(rf.read(), file2_expected_content)

    def run_recrypt_test(self,
                     action,
                     overwrite,
                     input_path=None,
                     key=None,
                     password=None,
                     clean_up=False):
        if not input_path:
            input_path = self.dir1

        if overwrite:
            output_path = None
            file1_path = self.file1
            file2_path = self.file2
        else:
            output_path = input_path + f'_{action}_output'
            file1_path = os.path.join(output_path, os.path.basename(self.file1))
            file2_path = os.path.join(output_path,
                                      os.path.basename(self.dir2),
                                      os.path.basename(self.file2))

        self.call_recrypt(action, input_path, output_path=output_path, key=key, password=password, overwrite=overwrite)
        if action == 'encrypt':
            self.make_assertions('not_equal', file1_path=file1_path, file2_path=file2_path)
        else:
            self.make_assertions('equal', file1_path=file1_path, file2_path=file2_path)

        if clean_up:
            shutil.rmtree(output_path)
            shutil.rmtree(input_path)
        else:
            return output_path

    def test_overwriting_with_password(self):
        self.run_recrypt_test(action='encrypt', overwrite=True, password=self.password)
        self.run_recrypt_test(action='decrypt', overwrite=True, password=self.password)

    def test_overwriting_with_key(self):
        self.run_recrypt_test(action='encrypt', overwrite=True, key=self.key)
        self.run_recrypt_test(action='decrypt', overwrite=True, key=self.key)

    def test_not_overwriting(self):
        output = self.run_recrypt_test(action='encrypt', overwrite=False, password=self.password)
        self.run_recrypt_test(action='decrypt', overwrite=False, input_path=output, password=self.password, clean_up=True)


if __name__ == '__main__':
    unittest.main()
