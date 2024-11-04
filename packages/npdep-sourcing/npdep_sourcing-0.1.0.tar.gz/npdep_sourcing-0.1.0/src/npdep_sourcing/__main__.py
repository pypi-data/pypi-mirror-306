import sys

import argparse

from npdep_sourcing.args.Args import Args
from npdep_sourcing.util.Util import Util
from npdep_sourcing.output.Output import Output

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

    print("This module does not provide any direct functionalty.")

    out.printExecutionTime()


if __name__ == "__main__":
    sys.exit(main())
