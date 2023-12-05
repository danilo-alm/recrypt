from utils.parser import args
from utils.crypto_handler import CryptoHandler
from utils.operation import Operation
import sys

crypto_handler = CryptoHandler(
    password=args.password,
    key=args.key
)

crypto_args = (
    args.input,  # input_path
    args.input if args.overwrite else args.output  # output_path
)

crypto_handler.encrypt(*crypto_args) if args.encrypt else crypto_handler.decrypt(*crypto_args)
