from parser import args
from crypto_handler import CryptoHandler
from operation import Operation
import sys

crypto_handler = CryptoHandler(
    password=args.password,
    key=args.key
)

crypto_args = (
    args.encrypt or args.decrypt,  # input_path
    (args.encrypt or args.decrypt) if args.overwrite else args.output  # output_path
)

crypto_handler.encrypt(*crypto_args) if args.encrypt else crypto_handler.decrypt(*crypto_args)
