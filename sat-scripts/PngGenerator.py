#!/usr/bin/python
import sys
import os
import getopt
from pyhdf import SD
import h5py
import numpy as np
import png
import itertools
import math


class PngGenerator:
    filename = ""
    mask_filename = ""
    calculation = ""
    out_filename = ""
    north = 90.0
    east = 180.0
    south = -90.0
    west = -180.0

    def __init__(
                self, filename, mask_filename, calculation, output,
                north=90.0, east=180.0, south=-90.0, west=-180.0
            ):
        self.filename = filename
        self.mask_filename = mask_filename
        self.calculation = calculation.replace('\\', '')
        self.out_filename = output
        self.north = north
        self.south = south
        self.east = east
        self.west = west
        self.palette = None
        self.data = None

    def set_coordinates(
                self, north=90.0, east=180.0, south=-90.0, west=-180.0
            ):
        self.north = north
        self.south = south
        self.east = east
        self.west = west

    def apply_mask(self, data):
        self.data = data
        mask_png = png.Reader(filename=self.mask_filename)
        column_count, row_count, mask, meta = mask_png.read()

        image_2d = np.vstack(itertools.imap(np.uint16, mask))
        print "Applying land mask"
        # This is the fastest
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                if (image_2d[i, j] > 251 or
                        data[i, j] <= 0 or
                        np.isnan(data[i, j]) or
                        math.isnan(data[i, j])):
                    data[i, j] = image_2d[i, j]
        self.palette = mask_png.palette()
        return self.data, self.palette

    def save_png(self, data, palette):
        print "Saving file"
        output = open(self.out_filename, 'wb')
        writer = png.Writer(data.shape[1], data.shape[0], palette=palette)
        writer.write(output, data)
        output.close()

    def cut_png(
                self, sds, new_north, new_east, new_south, new_west,
                top=255, bottom=0, no_data=np.NaN,
                valid_max=np.NaN, valid_min=np.NaN
            ):
        data = self.get_data(sds)

        height = data.shape[0]
        width = data.shape[1]

        delta_lat = (self.north - self.south) / height
        delta_lon = (self.east - self.west) / width

        # center coordinates of the corners
        lat_north = self.north-delta_lat / 2.
        lon_west = self.west+delta_lon / 2.

        lin_north = 1
        lin_south = height - 1
        pix_east = width - 1
        pix_west = 1

        new_north -= delta_lat / 2.
        new_south += delta_lat / 2.
        new_west += delta_lon / 2.
        new_east -= delta_lon / 2.

        # define the starting and ending pixel-line numbers
        #   for the box of interest
        tmp_spix = float((new_west - lon_west) / delta_lon)
        # tmp_spix = float(pix_west+(pix_east-pix_west)
        #   *(new_west-lon_west)/(lon_east-lon_west))
        spix = max([pix_west, round(tmp_spix)])
        tmp_epix = float((new_east - lon_west) / delta_lon) + 1
        # tmp_epix = float(pix_west+(pix_east-pix_west)
        #   *(new_east-lon_west)/(lon_east-lon_west))
        epix = min([pix_east, round(tmp_epix)])
        # tmp_slin = float(lin_south-(lin_south-lin_north)
        #   *(new_north-lat_south)/(lat_north-lat_south))
        tmp_slin = float((lat_north - new_north) / delta_lat)
        slin = max([lin_north, round(tmp_slin)])
        # tmp_elin = float(lin_south-(lin_south-lin_north)
        #       *(new_south-lat_south)/(lat_north-lat_south))
        tmp_elin = float((lat_north - new_south) / delta_lat) + 1
        elin = min([lin_south, round(tmp_elin)])

        data = data[slin: elin, spix: epix]  # data[0:height - 1,]

        if not np.isnan(valid_max):
            data[np.where(data > valid_max)] = no_data

        if not np.isnan(valid_min):
            data[np.where(data < valid_min)] = no_data

        no_data_positions = np.where(data == no_data)

        # Transform data to calculation
        exec "data=np.around(" + self.calculation + ")"

        if top != np.NaN:
            data[np.where(data > top)] = top

        if bottom != np.NaN:
            data[np.where(data < bottom)] = bottom

        if no_data_positions != np.NaN:
            data[no_data_positions] = 251

        data, palette = self.apply_mask(data)
        self.save_png(data, palette)

    def generate_png(
                self, sds_name, top=255, bottom=0, no_data=np.NaN,
                valid_max=np.NaN, valid_min=np.NaN
            ):
        data = self.get_data(sds_name)

        if not np.isnan(valid_max):
            data[np.where(data > valid_max)] = no_data

        if not np.isnan(valid_min):
            data[np.where(data < valid_min)] = no_data

        no_data_positions = np.where(data == no_data)

        # Transform data to calculation
        exec "data=np.around(" + self.calculation + ")"

        if top != np.NaN:
            data[np.where(data > top)] = top

        if bottom != np.NaN:
            data[np.where(data < bottom)] = bottom

        if no_data_positions != np.NaN:
            data[no_data_positions] = 251

        data, palette = self.apply_mask(data)
        self.save_png(data, palette)

    def get_data(self, sds_name):
        path, ext = os.path.splitext(self.filename)
        if ext in (".hdf", ".hdf4", ".HDF", ".HDF4"):
            return self.get_hdf_data(sds_name)
        elif ext in (".h5", ".H5"):
            return self.get_hdf5_data(sds_name)

    def get_hdf_data(self, sds_name):
        # open the hdf file for reading
        hdf = SD.SD(self.filename)
        # read the sds data
        sds_obj = hdf.select(sds_name)
        data = sds_obj.get()
        return data

    def get_hdf5_data(self, sds_name):
        # open the hdf5 file for reading
        hdf5 = h5py.File(self.filename, 'r')
        # read the sds data
        data = hdf5[sds_name][()]
        return data


def usage():
    print("-h --help  Display this help")
    print("-f --file  Input file")
    print("-o --output Output filename")
    print("-m --mask_file  File containing the png mask")
    print("-s --sds Name of the product to generate the png")
    print(
        "-c --calculation Equation to calculate the pixel to value relation, "
        "should include data keyword"
    )
    print("-t --top Top value to use in the color index")
    print("-b --bottom Bottom value to use in the color index")
    print("-n --no_data No data value")
    print("-u --max_data Maximum valid data value")
    print("-l --min_data Minimum valid data value")

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(
            sys.argv[1:], "hf:m:c:o:s:t:b:n:u:l:a:d:e:g:w:x:y:z:",
            [
                "help", "file=", "mask_file=", "calculation=", "output=",
                "sds=", "top=", "bottom=", "no_data", "max_data", "min_data"
            ]
        )
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    top = 255
    bottom = 0
    no_data = np.NaN
    max_data = np.NaN
    min_data = np.NaN

    original_north = np.NaN
    original_east = np.NaN
    original_south = np.NaN
    original_west = np.NaN

    north = np.NaN
    east = np.NaN
    south = np.NaN
    west = np.NaN

    user_calculation = "data"

    input_file = None
    mask_file = None
    output_file = None
    sds = None

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-f", "--file"):
            input_file = arg
        elif opt in ("-m", "--mask_file"):
            mask_file = arg
        elif opt in ("-c", "--calculation"):
            user_calculation = arg
        elif opt in ("-o", "--output"):
            output_file = arg
        elif opt in ("-s", "--sds"):
            sds = arg
        elif opt in ("-t", "--top"):
            top = float(arg)
        elif opt in ("-b", "--bottom"):
            bottom = float(arg)
        elif opt in ("-n", "--no_data"):
            no_data = float(arg)
        elif opt in ("-u", "--max_data"):
            if arg == 'NaN':
                max_data = np.NaN
            else:
                max_data = float(arg)
        elif opt in ("-l", "--min_data"):
            if arg == 'NaN':
                min_data = np.NaN
            else:
                min_data = float(arg)
        elif opt in "-a":
            original_north = float(arg)
        elif opt in "-d":
            original_east = float(arg)
        elif opt in "-e":
            original_south = float(arg)
        elif opt in "-g":
            original_west = float(arg)
        elif opt in "-w":
            north = float(arg)
        elif opt in "-x":
            east = float(arg)
        elif opt in "-y":
            south = float(arg)
        elif opt in "-z":
            west = float(arg)

    generator = PngGenerator(
        input_file, mask_file, user_calculation, output_file
    )
    if (not np.isnan(original_north) and
            not np.isnan(original_east) and
            not np.isnan(original_south) and
            not np.isnan(original_west) and
            not np.isnan(north) and
            not np.isnan(east) and
            not np.isnan(south) and
            not np.isnan(west)):
        generator.set_coordinates(
            original_north, original_east, original_south, original_west
        )
        generator.cut_png(
            sds, north, east, south, west, top, bottom, no_data,
            max_data, min_data
        )
    else:
        generator.generate_png(sds, top, bottom, no_data, max_data, min_data)
