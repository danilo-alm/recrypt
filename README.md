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

- `-e/--encrypt`: Encrypt the specified input directory or file.
- `-d/--decrypt`: Decrypt the specified input directory or file.

**Choose one of the following for output:**
- `-o/--output <directory/file>`: Specify the output directory or file for the encrypted/decrypted content.
- `--overwrite`: Overwrite the specified input directory or file with the encrypted/decrypted content.

**Choose one of the following for passkey:**
- `-k/--key <key>`: Use a specified 32 url-safe base64-encoded key for encryption/decryption.
- `-p/--password <password>`: Use a specified password for encryption/decryption.

**Positional Argument:**
- `input`: The file or directory name to be encrypted or decrypted.

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

## License

Recrypt is licensed under the [GNU General Public License v3.0](https://github.com/danilo-alm/recrypt/blob/main/LICENSE). You are free to modify and distribute this software in accordance with the terms of the license. For more details, please refer to the [full text of the license](https://www.gnu.org/licenses/gpl-3.0.html).

### Summary of the GNU GPL v3.0

- You are free to run, modify, and share the software.
- Any modifications you make must be released under the same license when distributing.
- This software is distributed without any warranty; refer to the license for details.
