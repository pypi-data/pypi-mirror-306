import sys

import argparse

from .args.Args import Args
from .util.Util import Util
from .output.Output import Output

def main(args_=None):
    """The main routine."""
    if args_ is None:
        args_ = sys.argv[1:]

    parser = argparse.ArgumentParser()
    Args.addArguments(parser)
    args = parser.parse_args()

    # Creates Output instance for printing header and footer of console output
    out = Output()
    out.printHeader()

    print("This module does not have any direct functionality usable via command line. \nIt does provide Reader class for reading Data Exfiltration Protocol bytes.")

    out.printExecutionTime()


if __name__ == "__main__":
    sys.exit(main())
