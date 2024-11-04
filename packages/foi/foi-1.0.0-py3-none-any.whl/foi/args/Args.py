import argparse

from foi.util.Util import Util

class Args():
    # parser: argparse instance
    def addArguments(parser):
        parser.add_argument("--path", "-p", type=str, required=True, help="Path which shall be searched.")
        parser.add_argument("--files", "-f", type=Util.createFileTypeList, default=["txt", "pdf", "png", "jpg"], help="Comma separated list of file type to be searched for: pdf,jpg,txt")