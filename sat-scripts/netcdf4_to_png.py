#!/usr/bin/python3
"""
creates a png from a given netCDF4 file & variable name.

requires matplotlib & netCDF4 (& tkinter)
`pip3 intstall matplotlib netcdf4`
`yum install python34-tkinter`  # from epel
"""
from argparse import ArgumentParser

import matplotlib
matplotlib.use('Agg')  # fixes "no display name and no $DISPLAY environment variable"
import matplotlib.pyplot as plt
import netCDF4

def main(args):
    nc = netCDF4.Dataset(args.in_path)
    plt.imshow(nc.variables[args.var_name])
    plt.savefig(args.out_path, bbox_inches=0)

if __name__ == "__main__":
    parser = ArgumentParser(description='output png from netCDF4 file')

    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="count",
                        default=0
    )
    parser.add_argument("in_path",  help="netCDF4 file path input")
    parser.add_argument("out_path", help="path of png to output")
    parser.add_argument("var_name", help="name of variable to output from netCDF4 file")
    args = parser.parse_args()
    main(args)
