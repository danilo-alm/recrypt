from parser import args
from crypto_handler import CryptoHandler
from operation import Operation
import sys


crypto_handler = CryptoHandler(
    operation=Operation.ENCRYPT if args.encrypt else Operation.DECRYPT,
    password=args.password,
    key=args.key
)

input_path = args.encrypt or args.decrypt

crypto_handler.handle_path(
    path=input_path,
    output_path=input_path if args.overwrite else args.output
)
