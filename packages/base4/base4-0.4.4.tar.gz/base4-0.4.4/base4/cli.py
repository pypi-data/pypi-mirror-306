import argparse
import sys
from base4 import d4decode, d4encode
def main() -> None:
    parser = argparse.ArgumentParser(description="base4 encoder/decoder")
    parser.add_argument(
        "--encode",
        action="store_true",
        help="Encode data",
    )
    parser.add_argument(
        "--decode",
        action="store_true",
        help="Decode data",
    )
    args = parser.parse_args()

    if args.encode:
        data = sys.stdin.buffer.read()
        sys.stdout.write(d4encode(data).decode())
    elif args.decode:
        data = sys.stdin.buffer.read()
        sys.stdout.buffer.write(d4decode(data.decode()))
    else:
        parser.print_help()
        sys.exit(1)
if __name__ == "__main__":
    main()
