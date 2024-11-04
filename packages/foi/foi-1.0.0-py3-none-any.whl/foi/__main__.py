import sys

import argparse

from foi.args.Args import Args
from foi.output.Output import Output
from foi.search.Search import Search

def main(args_=None):
    """The main routine."""
    if args_ is None:
        args_ = sys.argv[1:]

    parser = argparse.ArgumentParser()
    Args.addArguments(parser)
    args = parser.parse_args()

    out = Output()
    out.printHeader()
    out.printFileTypes(args.files)
    out.printPath(args.path)

    s = Search(args.files)
    paths = s.getFilePaths(args.path)

    out.printResult(paths)
    out.printExecutionTime()


if __name__ == "__main__":
    sys.exit(main())
