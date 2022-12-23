# import modules
import matplotlib.pyplot as plt
from rasterio.plot import show
import pandas as pd
import geopandas as gpd
import networkx as nx
import os
import json
import rasterio.plot
import math
import warnings
from shapely.geometry import Point
from flooding_function import naismith
warnings.simplefilter(action="ignore", category=FutureWarning)


# Create a graph for the ITN
# import data
# ITN data
itn_path = os.path.join("/Users/mariebourel/Documents/Fac/Master 2022_2023/UCL/cours/CEGE0096 - Geospatial Programming/2nd Assignment/Material/itn", "solent_itn.json") # week 8- practical
with open(itn_path, "r") as f:
    itn_json = json.load(f)

# Elevation Raster
# define elevation for each graph nodes: ASCII Grid file // British national grid // https://www.ordnancesurvey.co.uk/business-government/products/terrain-5
path_elevation = "/Users/mariebourel/Documents/Fac/Master 2022_2023/UCL/cours/CEGE0096 - Geospatial Programming/2nd Assignment/Material/elevation/SZ.asc"
elevation_data = rasterio.open(path_elevation)


# Format ITN roadlinks dataset
# get details of the itn roadlinks : British national grid
pd_itn = pd.DataFrame.from_dict(itn_json["roadlinks"], orient="index")
pd_itn = pd_itn.reset_index()
pd_itn = pd_itn.rename(columns={"index": "fid"})

# explode coords of all the points and create a column with next point
pd_itn_exp = pd_itn[["fid", "coords"]].explode("coords")
pd_itn_exp["next_pt"] = pd_itn_exp["coords"].groupby(pd_itn_exp["fid"]).shift(-1)
pd_itn_exp = pd_itn_exp.dropna()
pd_itn_exp = pd_itn_exp.rename(columns={"coords": "start_pt"})


# Extract from the Elevation raster, elevation for each ITN point
# extract coordinate (x,y) format not geom point // https://geopandas.org/en/stable/gallery/geopandas_rasterio_sample.html
coords_start_pt = [tuple(x) for x in pd_itn_exp["start_pt"]]
coords_next_pt = [tuple(x) for x in pd_itn_exp["next_pt"]]

# Sample the raster at every point location and store values in DataFrame
pd_itn_exp["Raster Value Start"] = [x[0] for x in elevation_data.sample(coords_start_pt)]
pd_itn_exp["Raster Value Next"] = [x[0] for x in elevation_data.sample(coords_next_pt)]


# Calculate difference of elevation: h
pd_itn_exp["h"] = pd_itn_exp["Raster Value Next"] - pd_itn_exp["Raster Value Start"]


# Calculate Distance between Points
# Convert tuple of coordinates to point
pd_itn_exp["start_pt"] = [Point(x[0], x[1]) for x in pd_itn_exp["start_pt"]]
pd_itn_exp["next_pt"] = [Point(x[0], x[1]) for x in pd_itn_exp["next_pt"]]

# Calculate distance between points // https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoSeries.distance.html
pd_itn_exp["distance"] = gpd.GeoSeries(pd_itn_exp["start_pt"]).distance(gpd.GeoSeries(pd_itn_exp["next_pt"]), align=False)

# Update links' weight
# update edges value with naismith function
pd_itn_exp["weight"] = pd_itn_exp.apply(lambda x: naismith(x.distance, x.h), axis=1)

# aggregate weight by roadlink id
df_roadlink = pd.DataFrame(pd_itn_exp[["fid", "weight"]].groupby("fid").sum("weight")).reset_index()
df_roadlink = df_roadlink.merge(pd_itn, on="fid")


# Create Directed Graph for ITN
# digraph
itn_digraph = nx.DiGraph()

for link in range(len(df_roadlink["fid"])):
    fid = df_roadlink.loc[link, "fid"]
    start_pt = df_roadlink.loc[link, "start"]
    end_pt = df_roadlink.loc[link, "end"]
    weight = df_roadlink.loc[link, "weight"]
    itn_digraph.add_edge(start_pt, end_pt, fid=link, weight=weight)

# nx.draw(itn_digraph, node_size=1)


# Define Shortest Path between Point
# Shortest path within the digraph
path = nx.dijkstra_path(itn_digraph, source="osgb4000000026141631", target="osgb4000000026126418", weight="weight")
path


# Export shortest path
nodes = gpd.read_file("/Users/mariebourel/Documents/Fac/Master 2022_2023/UCL/cours/CEGE0096 - Geospatial Programming/2nd Assignment/Material/roads/nodes.shp")
pt = nodes.merge(pd.DataFrame(path), right_on=0, left_on="fid")
pt = pt.rename(columns={0: "pathnod"})

pt.to_file("path.json", driver="GeoJSON")