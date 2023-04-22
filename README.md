# csv2sacs: Convert Metocean data into a SACS seastate input file

This repository contains two python scripts to (a) sanitise a CSV file, and (b) convert the sanitised CSV file into a SACS sea state input file. A version of this readme is available as [a standalone PDF file](./README.pdf).

## Scope

The stand-alone script, `slc.py` converts Metocean data into a readily usable SACS input file.[^1]

The script, written in python scripting language, requires some user inputs. These can be keyed-in by editing the block of data within `BEGIN USER INPUTS` and `END USER INPUTS` in the script file `slc.py`, set pre-determined values (or defaults) as appropriate, and provide a comma separated data file (CSV) from Metocean at command line. For help, run script(s) as follows:

```sh
python3 fdf.py --help
python3 slc.py --help
```

The SACS seastate input file may be generated in two steps:

```sh
python3 fdf.py -f <csv file>
```

followed by

```sh
python3 slc.py -f <formatted csv file> > seastate.inp
```

If there is more than one CSV file, then here is an easier way to batch generate seastate input files:

```sh
for FILE in *.csv; do python3 ./fdf.py -f $FILE; done
for FILE in F*.csv; do python3 ./slc.py -f $FILE > $FILE.inp; done
```

Note: In the above, if the given Metocean data csv file name is, say, `text.csv`, then the formatted CSV file name becomes `Ftest.csv`.

## Requirements

The script requires the following and can be run at command line interface with the following installed and available:

1. python v3 scripting language,
1. pandas data analysis library,
1. docopt command-line interface description language

Install the required python modules like so:

```sh
python3 -m pip install --upgrade docopt pandas
```

## Limitation and workarounds

The limitations of the script are (a) only the system memory allocated for the script, and (b) SACS's four character field for load cases. In other words for load cases greater than `9999`, the load case numbering will default back to `0000`. This can be overcome by splitting the data file to be less than `9999` load cases.

## CSV file format

```csv
,H (m), T(s), WS (m/s), CS5(m/s), CS20(m/s), CS30(m/s), CS50(m/s), CS70(m/s), CS90(m/s), CS110(m/s), CS130(m/s), CS150(m/s), CS170(m/s)
4.48,14.56,290.0,0.75,0.68,0.6,0.5,0.44,0.41,0.35,0.3,0.25,0.15,
4.81,14.67,290.0,0.75,0.68,0.6,0.5,0.44,0.41,0.35,0.3,0.25,0.15,
4.4,14.21,290.0,0.75,0.68,0.6,0.5,0.44,0.41,0.35,0.3,0.25,0.15,
4.18,12.34,290.0,0.75,0.68,0.6,0.5,0.44,0.41,0.35,0.3,0.25,0.15,
2.83,8.32,290.0,0.75,0.68,0.6,0.5,0.44,0.41,0.35,0.3,0.25,0.15,
3.76,14.89,290.0,0.75,0.68,0.6,0.5,0.44,0.41,0.35,0.3,0.25,0.15,
6.07,14.04,290.0,0.75,0.68,0.6,0.5,0.44,0.41,0.35,0.3,0.25,0.15,
...
```

## Sample output

```
# Reading FTS001.000040TS.csv file...done.
FILE B
LOADCN   1
LOADLB   1Envir for pile storm analysis
WAVE
WAVE0.95STOK  4.48       14.56         290.0      D  -90.0   4.0  90MM10 1
CURR
CURR        1.18    0.15   290.0                        BC NL         AWP
CURR       21.18    0.25   290.0
CURR       41.18     0.3   290.0
CURR       61.18    0.35   290.0
CURR       81.18    0.41   290.0
CURR      101.18    0.44   290.0
CURR      121.18     0.5   290.0
CURR      141.18     0.6   290.0
CURR      151.18    0.68   290.0
CURR      166.18    0.75   290.0
LOADCN   2
LOADLB   2Envir for pile storm analysis
WAVE
WAVE0.95STOK  4.81       14.67         290.0      D  -90.0   4.0  90MM10 1
CURR
CURR        1.18    0.15   290.0                        BC NL         AWP
CURR       21.18    0.25   290.0
CURR       41.18     0.3   290.0
...
CURR      151.18    0.75   185.0
CURR      166.18    0.83   185.0
LOADCN7931
LOADLB7931Envir for pile storm analysis
WAVE
WAVE0.95STOK  6.63       11.36         185.0      D  -90.0   4.0  90MM10 1
CURR
CURR        1.18    0.17   185.0                        BC NL         AWP
CURR       21.18    0.28   185.0
CURR       41.18    0.33   185.0
CURR       61.18    0.39   185.0
CURR       81.18    0.45   185.0
CURR      101.18    0.48   185.0
CURR      121.18    0.55   185.0
CURR      141.18    0.67   185.0
CURR      151.18    0.75   185.0
CURR      166.18    0.83   185.0
```

## Trivia

At work, we've been looking to determine cyclic axial capacity of a fixed platform's drilled and grouted foundations in calcareous soils from storm time-history sets.[^1] The team is looking to generate pile loads from this using Bentley's SACS analysis suite. When totalled it adds to upwards of 30,000 discreet load cases.

With the archaic fixed-format, SACS is unfriendly to developing user-input files especially by hand, and in our case seastate load input file(s). With 8,000 load cases, this requires generating about 127,000 unique lines of input, per history, error-free. Manually this is impracticable.

Volunteering to automate this, I got the script `slc.py` working, which converts thousands lines of Metocean data comma separated value (CSV) files into hundreds of thousands of SACS input lines. The script does this in seconds. It is very specific to the structure of the CSV file and the order in which data parameters occur. The first three columns represent wave data (height, period, and direction), and the last ten columns (to be aligned with `eam` list) represent current speed at ten intervals from water surface to seabed in decreasing order.[^2] However, SACS requires this to be input in the increasing order, and therefore the ranges are reversed (aligned with `eam`) and in negative increments to get appropriate column indices. Other than that, this script just re-prints data from the dataframe in a fixed format that SACS requires. Here's how it works:

1. Loads the data from a CSV file, input at command line, into a dataframe
2. Prints a line `FILE B` for a standalone seastate file
3. Commences a loop for all lines in the CSV file, where each line is a load case
4. Prints `WAVE` cards from wave data in the first three columns
5. Prints `CURR` cards (incl. a multi-line local loop) from current data

There is of course an opportunity to make this script generic (e.g., by updating the script to automatically count columns from either side and generate column index accordingly for further use) so that there is no need to re-factor the code --- should the data structure change, but this code solved our immediate problem.

[^1]: The approach is described in a paper titled [Axial and lateral pile design in carbonate soils][p] by C.T. Erbrich, M.P. O'Neill, P. Clancy, M.F. Randolph, _Axial and lateral pile design in carbonate soils_, The University of Western Australia, 2010.

[^2]: If current profile changes, then this script will require editing --- specifically to hardcoded current-specific indices at (a) the fourth print line (`# col 9-16`), (b) the fifth print line (`# col 17-24`), (c) the `range()` parameters, and (d) the elevation above mudline user input list `eam`.

[p]: https://research-repository.uwa.edu.au/en/publications/axial-and-lateral-pile-design-in-carbonate-soils "C.T. Erbrich, et al., UWA, 2010."
[pandas]: https://pandas.pydata.org "A fast, powerful, flexible and easy to use open source data analysis and manipulation tool, built on top of the Python programming language."
