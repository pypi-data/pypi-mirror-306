import sys

import argparse

from .args.Args import Args
from .converter.Converter import Util
from .output.Output import Output

def main(args_=None):
    """The main routine."""
    if args_ is None:
        args_ = sys.argv[1:]

    # Creates Output instance for printing header and footer of console output
    out = Output()
    out.printHeader()

    print("This module does not have any direct functionalty. \nIt does only provide common types and capabilites to dep_client and dep_reader.")

    out.printExecutionTime()


if __name__ == "__main__":
    sys.exit(main())
