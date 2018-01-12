#!/usr/bin/python3
"""
creates a png from a given netCDF4 file & variable name.

requires matplotlib & netCDF4 (& tkinter)
`pip3 intstall matplotlib netcdf4`
`yum install python34-tkinter`  # from epel

example usage:
-------------
./sat-scripts/netcdf4_to_png.py \
/srv/imars-objects/modis_aqua_gom/l3/2017-12-17T12:00:00Z_l3.nc \
test_chlor_a.png \
chlor_a
"""
from argparse import ArgumentParser

import matplotlib
matplotlib.use('Agg')  # fixes "no display name and no $DISPLAY environment variable"
import matplotlib.pyplot as plt
import netCDF4
import numpy as np

def main(args):
    nc = netCDF4.Dataset(args.in_path)
    # plt.imshow(nc.variables[args.var_name])
    # plt.savefig(args.out_path, bbox_inches=0)
    try:
        data = np.array(nc.variables[args.var_name])
    except KeyError as k_err:
        raise KeyError('variable not found in netcdf4 file "' + args.var_name + 
                       '". Variables available: ' + str(list(nc.variables))
        )
    data = eval("np.around(" + args.transform + ")")
    plt.imsave(
        args.out_path, data,
        vmin=0,
        vmax=255,
        cmap=plt.get_cmap("nipy_spectral")
    )

if __name__ == "__main__":
    parser = ArgumentParser(description='output png from netCDF4 file')

    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="count",
                        default=0
    )
    parser.add_argument("in_path",  help="netCDF4 file path input")
    parser.add_argument("out_path", help="path to output file, including file extension for desired output format.")
    parser.add_argument("var_name", help="name of variable to output from netCDF4 file")
    parser.add_argument(
        "-t", "--transform", default="data",
        help="Transform to apply to data before export. Example: 'np.log10(data+1)/0.00519'"
    )
    args = parser.parse_args()
    main(args)
