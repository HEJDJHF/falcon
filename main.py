import os
import rasterio
from rasterio import plot

from user_input import user_input
from clip_raster_file import clip_raster_file


def main():
    easting = float(input('Please enter the Easting of your current location: '))
    northing = float(input('Please enter the Northing of your current location: '))

    user_location, is_on_land = user_input(easting, northing)
    if is_on_land:
        clip_raster_file(easting, northing)
    else:
        exit(main)

    #  Internal note: This part can be removed. I left it in for easy reference on what the output looks like.
    new_dataset = rasterio.open(os.path.join('Material', 'elevation', 'output_SZ.asc'))
    rasterio.plot.show(new_dataset)

if __name__ == '__main__':
    main()