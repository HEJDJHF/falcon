import os
import rasterio
from rasterio import plot

from user_input import user_input
from clip_raster_file import clip_raster_file


def main():
    print('Insert user location:')
    while True:
        try:
            easting = float(input('Easting: '))
            northing = float(input('Northing: '))
            break
        except ValueError:
            print('Please enter a number. Try again.')

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
