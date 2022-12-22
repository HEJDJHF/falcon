import os
from shapely.geometry import Point
import rasterio
from rasterio.mask import mask


#  This function clips out the raster data within 5km from the user's location, transforms the clipped data
#  into the correct coordinate reference system, and saves it as a new file "output_SZ.asc".

def clip_raster_file(easting, northing):
    user_location = Point(easting, northing)
    polygon = user_location.buffer(5000)
    dataset = rasterio.open(os.path.join('Material', 'elevation', 'SZ.asc'))
    clipped_dataset, out_transform = mask(dataset, [polygon], all_touched=True, crop=True)
    out_meta = dataset.meta.copy()
    out_meta.update({"driver": "GTiff",
                     "height": clipped_dataset.shape[1],
                     "width": clipped_dataset.shape[2],
                     "transform": out_transform})
    with rasterio.open(os.path.join('Material', 'elevation', 'output_SZ.asc'), 'w', **out_meta) as dst:
        dst.write(clipped_dataset)
