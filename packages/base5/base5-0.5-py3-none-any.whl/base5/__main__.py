import argparse
import sys
from typing import Callable, Dict, Tuple
from base5 import d5decode, d5decode_check, d5encode, d5encode_check
_fmap = {
    (False, False): d5encode,
    (False, True): d5encode_check,
    (True, False): d5decode,
    (True, True): d5decode_check
}
def main() -> None:
    stdout = sys.stdout.buffer
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument(
        'file',
        metavar='FILE',
        nargs='?',
        type=argparse.FileType('r'),
        default='-')
    parser.add_argument(
        '-d', '--decode',
        action='store_true',
        help='decode data')
    parser.add_argument(
        '-c', '--check',
        action='store_true',
        help='append a checksum before encoding')
    args = parser.parse_args()
    fun = _fmap[(args.decode, args.check)]
    data = args.file.buffer.read()
    try:
        result = fun(data)
    except Exception as e:
        sys.exit(e)
    stdout.write(result)
if __name__ == '__main__':
    main()
