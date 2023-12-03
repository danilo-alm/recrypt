from tempfile import mkdtemp, mkstemp
import subprocess
import unittest
import shutil
import os


class TestRecrypt(unittest.TestCase):
    
    def create_temp_file(self, filename, content, directory=None):
        file_handle, file_path = mkstemp(dir=directory)
        file_handle.write(content) 
        file_handle.close()
        return file_path

    def setUp(self):
        self.dir1 = mkdtemp()
        self.dir2 = mkdtemp(dir=dir1)

        self.file1_content = str.encode('I hope you have a nice day')
        self.file2_content = str.encode('I hope you have a nice day too')

        self.file1 = self.create_temp_file('file1', file1_content, directory=dir1)
        self.file2 = self.create_temp_file('file2', file2_content, directory=dir2)
    
    def tearDown(self):
        shutil.rmtree(self.dir1)
