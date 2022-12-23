import os
from shapely.geometry import Point
from shapely.geometry import Polygon
import geopandas as gpd


def user_input(easting, northing):
    user_location = Point(easting, northing)

    #  OOP has been used to define the MBR and isle of wight polygons. The MBR has been set to the limits of the raster
    #  file as there is no error when clipping the raster file using rasterio's mask function (i.e. no need to cater
    #  for a 5km buffer).
    mbr = Polygon([(425000, 75000), (425000, 100000), (470000, 100000), (470000, 75000)])
    shapefile = gpd.read_file(os.path.join('Material', 'shape', 'isle_of_wight.shx'))

    if mbr.contains(user_location) and shapefile.contains(user_location)[0]:
        is_on_land = True
    elif mbr.contains(user_location) == True and shapefile.contains(user_location)[0] == False:
        print("Please check your coordinates. The location is out at sea.")
        is_on_land = False
    else:
        print("Please check your coordinates. The location does not fall within the region.")
        is_on_land = False

    return user_location, is_on_land
