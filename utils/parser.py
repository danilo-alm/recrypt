import argparse

parser = argparse.ArgumentParser(
    prog='Recrypt',
    description='Recrypt is a tool for encrypting and decrypting directories recursively',
)

action = parser.add_mutually_exclusive_group(required=True)
action.add_argument('-e', '--encrypt', action='store_true', help='Encrypt a directory/file')
action.add_argument('-d', '--decrypt', action='store_true', help='Decrypt a directory/file')

overwrite = parser.add_mutually_exclusive_group(required=True)
overwrite.add_argument('-o', '--output', type=str, help='Output directory/file')
overwrite.add_argument('--overwrite', action='store_true', help='Overwrite directory/file')

passkey = parser.add_mutually_exclusive_group(required=True)
passkey.add_argument('-k', '--key', type=str, help='Key to encrypt/decrypt')
passkey.add_argument('-p', '--password', type=str, help='Password to encrypt/decrypt')

parser.add_argument('input', type=str, help='Input directory/file')

args = parser.parse_args()
