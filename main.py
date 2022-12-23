"""
CEGE0096: Flood Emergency Planning
Extreme flooding is expected on the Isle of Wight and the authority in charge of planning the emergency response
is advising everyone to proceed by foot to the nearest high ground. To support this process, the emergency response
authority wants you to develop a software to quickly advise people of the quickest route that they should take to walk
to the highest point of land within a 5km radius.

6 tasks:
    - Task 1: User Input
    - Task 2: Highest Point Identification
    - Task 3: Nearest Integrated Transport Network
    - Task 4: Shortest Path
    - Task 5: Map Plotting
    - Task 6: Extend the Region
"""

# Import modules
import os
import rasterio
from rasterio import plot

from user_input import user_input
from clip_raster_file import clip_raster_file


def main():
    # user input
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