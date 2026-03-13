# ISMIP7 time encoding

## General guidance
For state variables snapshots are registered at the end of year.

For flux variables, yearly averages are registered to the middle of the year. Time bounds span from the beginning to the end of the year.

We use the standard (gregorian) CF calendar and record days since 1850.

## Calculate number of days for standard/gregorian calendar
python calc_days.py

## This produces the following files that can be used as templates:
days-since-1850.csv
days-since-1850_FL.nc
days-since-1850_ST.nc
