#!/usr/bin/python3
"""
lists variable keys from a given netCDF4 file.

requires matplotlib & netCDF4.
"""
from argparse import ArgumentParser

import matplotlib.pyplot as plt
import netCDF4

def list_vars(args):
    nc = netCDF4.Dataset(args.in_path)
    for key in nc.variables.keys():
        print(key)

if __name__ == "__main__":
    parser = ArgumentParser(description='lists variable keys from a given netCDF4 file')

    parser.add_argument("in_path",  help="netCDF4 file path input")
    args = parser.parse_args()
    list_vars(args)
