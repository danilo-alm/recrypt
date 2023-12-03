import argparse

parser = argparse.ArgumentParser(
    prog='Recrypt',
    description='Recrypt is a tool for encrypting and decrypting directories recursively',
)

action = parser.add_mutually_exclusive_group(required=True)
action.add_argument('-e', '--encrypt', type=str, help='Encrypt a directory/file')
action.add_argument('-d', '--decrypt', type=str, help='Decrypt a directory/file')

overwrite = parser.add_mutually_exclusive_group(required=True)
overwrite.add_argument('-o', '--output', type=str, help='Output directory/file')
overwrite.add_argument('--overwrite', action='store_true', help='Overwrite directory/file')

parser.add_argument('-p', '--password', type=str, help='Password to encrypt/decrypt', required=True)

args = parser.parse_args()
