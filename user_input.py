from shapely.geometry import Point
from shapely.geometry import Polygon
import geopandas as gpd


def user_input(easting, northing):
    user_location = Point(easting, northing)
    #  The mbr has been set to the limits of the raster file as there is no error when clipping the raster file using
    #  rasterio's mask function.
    mbr = Polygon([(425000, 75000), (425000, 100000), (470000, 100000), (470000, 75000)])
    shapefile = gpd.read_file(r"C:\Users\GTX1650\OneDrive\Documents\UCL - Hydrographic Survey\CEGE0096 - Geospatial "
                              r"programming\Coursework 2\Emergency Planning for Floods\flood-emergency-planning-falcon"
                              r"\Material\shape\isle_of_wight.shx")

    #  The mbr here is unnecessary since there is no need to cater for a 5km buffer. More important is to ensure
    #  that the point lies on land.
    if mbr.contains(user_location) and shapefile.contains(user_location)[0]:
        is_on_land = True
    elif mbr.contains(user_location) == True and shapefile.contains(user_location)[0] == False:
        print("The point does not lie on land.")
        is_on_land = False
    else:
        print("The location does not fall within the region.")
        is_on_land = False

    return user_location, is_on_land
