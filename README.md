# Recrypt

Recrypt is a command-line tool designed to encrypt and decrypt directories recursively, encrypting each individual file within the specified directory and its subdirectories.

## Installation

Clone the repository and install the necessary dependencies using the following commands:

```bash
git clone https://github.com/danilo-alm/recrypt
cd recrypt
pip install -r requirements.txt
```

## Usage

To use Recrypt, invoke the program through the command line with the following arguments:

```bash
python recrypt.py [-e/--encrypt | -d/--decrypt] <directory/file> [-o/--output | --overwrite] [-k/--key | -p/--password] 
```

### Arguments

- `-e/--encrypt`: Encrypt the specified directory or file.
- `-d/--decrypt`: Decrypt the specified directory or file.
  
**Choose one of the following for output:**
- `-o/--output <directory/file>`: Specify the output directory or file for the encrypted/decrypted content.
- `--overwrite`: Overwrite the original directory or file with the encrypted/decrypted content.

**Choose one of the following for passkey:**
- `-k/--key <key>`: Use a specified 32 url-safe base64-encoded key for encryption/decryption.
- `-p/--password <password>`: Use a specified password for encryption/decryption.

### Examples

Encrypt a directory with a specific key:

```bash
python recrypt.py -e /path/to/directory -o encrypted_directory -k my_secret_key
```

Decrypt a file with a password, overwriting its original content:

```bash
python recrypt.py -d /path/to/file --overwrite -p my_password
```

For additional help, use:

```bash
python recrypt.py -h
```

## Note

- Make sure to keep your key or password secure, as it will be required for decryption.
- Use the `--overwrite` option with caution, as it will replace the original files with their encrypted/decrypted versions.
