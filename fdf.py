#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Format CSV file with Pandas
fdf.py 2022 ckunte

Usage: fdf.py (-f <file>)
       fdf.py --help
       fdf.py --version

Options:
  -h, --help  Show this help
  -f --file   Specify CSV input file to format (required)

"""
import pandas as pd
from docopt import docopt


def main(*args):
    print("# Reading " + datfile + " file...", end="")
    df = pd.read_csv("./" + datfile)
    print("done.")
    # remove wind speed column from data (by index -- this is a workaround:
    # [should be [3], but somehow [2] works -- possibly a python 3.8.10 bug)
    df2 = df.drop(df.columns[[2]], axis=1)
    return df2.to_csv("F" + datfile)


if __name__ == "__main__":
    args = docopt(
        __doc__, version="Generate SACS storm load cards from a CSV file, v0.1"
    )
    datfile = "%s" % (args["<file>"])
    main(datfile)
    print("Formatted file:", "F" + datfile)
