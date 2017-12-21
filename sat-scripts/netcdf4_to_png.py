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

# import matplotlib
# matplotlib.use('Agg')  # fixes "no display name and no $DISPLAY environment variable"
# import matplotlib.pyplot as plt
import png
try:
    from itertools import imap  # py2
except ImportError:
    imap=map  # py3
import math
import netCDF4
import numpy as np

def main(args):
    nc = netCDF4.Dataset(args.in_path)
    data = np.array(nc.variables[args.var_name])
    data = eval("np.around(" + args.transform + ")")
    # === w/ imshow
    # plt.imshow(data)
    # plt.savefig(args.out_path, bbox_inches=0)
    # === w/ imsave
    # plt.imsave(
    #     args.out_path, data, format='png'
    #     # vmin=0,
    #     # vmax=254
    #     # cmap=plt.get_cmap("Greens")
    # )
    # === w/ png
    mask_png = png.Reader(filename="./masks/chlor_a_gcoos_mask.png")
    column_count, row_count, mask, meta = mask_png.read()
    palette = mask_png.palette()
    image_2d = np.vstack(imap(np.uint16, mask))
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            if (image_2d[i, j] > 251 or
                    data[i, j] <= 0 or
                    np.isnan(data[i, j]) or
                    math.isnan(data[i, j])):
                data[i, j] = image_2d[i, j]
    with open(args.out_path, 'wb') as output:
        writer = png.Writer(data.shape[1], data.shape[0], palette=palette)
        writer.write(output, data)

if __name__ == "__main__":
    parser = ArgumentParser(description='output png from netCDF4 file')

    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="count",
                        default=0
    )
    parser.add_argument("in_path",  help="netCDF4 file path input")
    parser.add_argument("out_path", help="path of png to output")
    parser.add_argument("var_name", help="name of variable to output from netCDF4 file")
    parser.add_argument(
        "-t", "--transform", default="data",
        help="Transform to apply to data before export. Example: 'np.log10(data+1)/0.00519'"
    )
    args = parser.parse_args()
    main(args)
