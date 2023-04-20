#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Generate SACS storm load cards from a CSV file
slc.py 2022 ckunte

Tested for python v3.8.10, v3.10.8 with pandas >= v1.5.1

Usage: slc.py (-f <file>)
       slc.py --help
       slc.py --version

Options:
  -h, --help  Show this help
  -f --file   Specify CSV input file (required)

"""
import pandas as pd
from docopt import docopt


def main(*args):
    print("# Reading " + datfile + " file...", end="")
    df = pd.read_csv("./" + datfile)
    print("done.")
    print("FILE B")
    for i in range(len(df)):
        # PRINTING WAVE INPUT LINES
        print(f"LOADCN{i+1:4}")
        print(f"LOADLB{i+1:4}Envir for pile storm analysis")
        print(W[0])
        print(
            f"{W[0]:4}"  # col 1-4, line label
            + f"{W[1]:4}"  # col 5-8, kinematics fac.
            + f"{W[2]:4}"  # col 9-12, wave type
            + f"{df.iat[i, 0]:>6}"  # col 13-18, wave height
            + f"{F[0]:>6}"  # col 19-24, SWL, skip (from LDOPT)
            + f"{df.iat[i, 1]:>6}"  # col 25-30, wave period
            + f"{F[0]:>8}"  # col 31-38, wave length, skip if period is given
            + f"{df.iat[i, 2]:>6}"  # col 39-44, wave angle
            + f"{F[0]:>6}"  # col 45-50, mud line elev., skip (from LDOPT)
            + f"{W[3]:>0}"  # col 51, input mode
            + f"{W[4]:>7}"  # col 52-58, crest position
            + f"{W[5]:>6}"  # col 59-64, step size
            + f"{F[0]:1}"  # col 65-66, steps for dyn. analysis, skip
            + f"{W[6]:1}"  # col 67-68, static steps
            + f"{W[7]:1}"  # col 69-70, critical position
            + f"{W[8]:1}"  # col 71-72, member seg. (max)
            + f"{W[9]:1}"  # col 73-74, member seg. (min)
            # + "{0:0}".format(F[0])  # col 75, local accel. only, skip
            # + "{0:0}".format(F[0])  # col 76, print opt, skip
            # + "{0:<1}".format(F[0])  # col 77-78, order of stream func., skip
        )
        # PRINTING CURRENT INPUT LINES
        print(C[0])
        print(
            f"{C[0]:4}"  # col 1-4, line label
            + f"{F[0]:>4}"  # col 5-8, min inline curr velocity, skip
            + f"{eam[9]:>8}"  # col 9-16, elev above mud line
            + f"{df.iat[i, 12]:>8}"  # col 17-24, curr velocity
            + f"{df.iat[i, 2]:>8}"  # col 25-32, curr dir
            + f"{F[0]:>8}"  # col 33-40, mudline elev override, skip
            + f"{F[0]:>8}"  # col 41-48, blocking factor, skip
            + f"{F[0]:>8}"  # col 49-56, elev, skip
            + f"{C[1]:1}"  # col 57-58, elev, generate blocking fac.
            + f"{F[0]:>0}"  # col 59, null
            + f"{C[2]:1}"  # col 60-61, crest stretching opt.
            + f"{F[0]:>0}"  # col 62, null
            + f"{F[0]:2}"  # col 63-65, velocity units opt., skip
            + f"{F[0]:>0}"  # col 66, null
            + f"{F[0]:2}"  # col 67-69, elev percent opt., skip
            + f"{F[0]:>3}"  # col 70, null (for now this is a workaround)
            + f"{C[3]:>2}"  # col 71-73, AWP opt.
        )
        # adjust ranges depending upon the current profile
        for n, m in zip(range(8, -1, -1), range(11, 2, -1)):
            print(
                f"{C[0]}"  # col 1-4, line label
                + f"{F[0]:>4}"  # col 5-8, min inline curr velocity, skip
                + f"{eam[n]:>8}"  # col 9-16, elev above mud line
                + f"{df.iat[i, m]:>8}"  # col 17-24, curr velocity
                + f"{df.iat[i, 2]:>8}"  # col 25-32, curr dir
            )
    pass


if __name__ == "__main__":
    args = docopt(
        __doc__, version="Generate SACS storm load cards from a CSV file, v0.1"
    )
    datfile = "%s" % (args["<file>"])
    #
    # -- BEGIN USER INPUTS --
    #
    # WAVE DEFINITION AND POSITION PARAMETERS (SACS SEASTATE MANUAL, PG 170)
    #
    W = [
        "WAVE",  # line label
        0.95,  # kinematics factor
        "STOK",  # wave type
        "D",  # input mode (length (L), degree (D), or time (T))
        -90.0,  # crest position -- wave
        4.00,  # step size -- wave
        " 90",  # static steps -- wave
        "MM",  # critical position -- wave
        "10",  # member segmentation (max)
        " 1",  # member segmentation (min)
    ]
    # CURRENT PARAMETERS (SACS SEASTATE MANUAL, PG 171)
    #
    C = [
        "CURR",  # line label
        "BC",  # option to generate blocking factor
        "NL",  # crest stretching option
        "AWP",  # apparent wave period option
    ]
    # ELEVATION ABOVE MUDLINE (FOR CURRENT PROFILE)
    #
    eam = [
        166.18,
        151.18,
        141.18,
        121.18,
        101.18,
        81.18,
        61.18,
        41.18,
        21.18,
        1.18,
    ]
    # FILLER FOR EMPTY (OR NULL) COLUMN BLOCKS
    #
    F = [" "]
    #
    # CSV DATA FILE FROM METOCEAN TO USE
    #
    # Headers in CSV file:
    # H (m), T(s), ThetaP PlatformNth(Deg), WS (m/s), CS5(m/s),  CS20(m/s),  CS30(m/s),  CS50(m/s),  CS70(m/s),  CS90(m/s), CS110(m/s), CS130(m/s), CS150(m/s), CS170(m/s)

    # -- END USER INPUTS --

    main(datfile, W, F, C)
