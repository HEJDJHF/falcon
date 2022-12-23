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
warnings.simplefilter(action="ignore", category=FutureWarning)


# Transportation network: ITN
# isle_of_wight_itn_json = os.path.join("Material", "itn", "solent_itn.json")
isle_of_wight_itn_json = "/Users/mariebourel/Documents/Fac/Master 2022_2023/UCL/cours/CEGE0096 - Geospatial Programming/2nd Assignment/Material/itn/solent_itn.json"
with open(isle_of_wight_itn_json, "r") as f:
    solent_itn = json.load(f)
g = nx.Graph()
road_links = solent_itn["roadlinks"]
for link in road_links:
    g.add_edge(road_links[link]["start"], road_links[link]["end"], fid=link, weight=road_links[link]["length"])
nx.draw(g, node_size=1)
plt.show()

# Elevation Raster
# elevation = rasterio.open("/Users/mariebourel/Documents/Fac/Master 2022_2023/UCL/cours/CEGE0096 - Geospatial Programming/2nd Assignment/Material/elevation/SZ.asc")
# elevation.bounds  # BoundingBox(left=425000.0, bottom=75000.0, right=470000.0, top=100000.0)
# show(elevation)

# Create a graph for the ITN
# import data for the graph
itn_path = os.path.join("/Users/mariebourel/Documents/Fac/Master 2022_2023/UCL/cours/CEGE0096 - Geospatial Programming/2nd Assignment/Material/itn", "solent_itn.json") # week 8- practical
with open(itn_path, "r") as f:
    itn_json = json.load(f)

# digraph
itn_digraph = nx.DiGraph()
road_links = itn_json["roadlinks"]
for link in road_links:
    itn_digraph.add_edge(road_links[link]["start"], road_links[link]["end"], fid=link, weight=road_links[link]["length"])

# nx.draw(itn_digraph, node_size=1)


# Naismith rule
# time = distance x speed
# speed = distance / time

# knows:
#   - distance between the point
#   - elevation

# needed:
#   - slope = sin distance / elevation
#   - distance on the plan

def naismith(distance, elevation): # https://medium.com/@sunside/naismith-aitken-langmuir-tranter-and-tobler-modeling-hiking-speed-4ff3937e6898
    # slope = sin(length / elevation)
    if elevation > 0:
        # dist_plane = math.sqrt(distance ** 2 + elevation ** 2)
        length = math.sqrt(distance ** 2 + elevation ** 2) / 1000 # distance between two point on the surface converted into meters
        t = length * (1 / 5) + elevation * (1 / 0.6)
    else:
        length = math.sqrt(distance ** 2 + elevation ** 2) / 1000
        t = length * (1 / 5)
    # w = dist_plane / t
    return t


# define elevation for each graph nodes: ASCII Grid file // British national grid // https://www.ordnancesurvey.co.uk/business-government/products/terrain-5
path_elevation = "/Users/mariebourel/Documents/Fac/Master 2022_2023/UCL/cours/CEGE0096 - Geospatial Programming/2nd Assignment/Material/elevation/SZ.asc"
elevation_data = rasterio.open(path_elevation)

rasterio.plot.show(elevation_data)

# get details of the itn roadlinks : British national grid
pd_itn = pd.DataFrame.from_dict(itn_json["roadlinks"], orient="index")
pd_itn = pd_itn.reset_index()
pd_itn = pd_itn.rename(columns={"index": "fid"})

# developp coords of all the points and create a column with next point
pd_itn_exp = pd_itn[["fid", "coords"]].explode("coords")
pd_itn_exp["next_pt"] = pd_itn_exp["coords"].groupby(pd_itn_exp["fid"]).shift(-1)
pd_itn_exp = pd_itn_exp.dropna()
pd_itn_exp = pd_itn_exp.rename(columns={"coords": "start_pt"})

# extract coordinate (x,y) format not geom point // https://geopandas.org/en/stable/gallery/geopandas_rasterio_sample.html
coords_start_pt = [tuple(x) for x in pd_itn_exp["start_pt"]]
coords_next_pt = [tuple(x) for x in pd_itn_exp["next_pt"]]

# Sample the raster at every point location and store values in DataFrame
pd_itn_exp["Raster Value Start"] = [x[0] for x in elevation_data.sample(coords_start_pt)]
pd_itn_exp["Raster Value Next"] = [x[0] for x in elevation_data.sample(coords_next_pt)]

# Calculate diffrence of elevation: h
pd_itn_exp["h"] = pd_itn_exp["Raster Value Next"] - pd_itn_exp["Raster Value Start"]

# Convert tuple of coordinates to point
pd_itn_exp["start_pt"] = [Point(x[0], x[1]) for x in pd_itn_exp["start_pt"]]
pd_itn_exp["next_pt"] = [Point(x[0], x[1]) for x in pd_itn_exp["next_pt"]]

# Calculate distance between points // https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoSeries.distance.html
pd_itn_exp["distance"] = gpd.GeoSeries(pd_itn_exp["start_pt"]).distance(gpd.GeoSeries(pd_itn_exp["next_pt"]), align=False)

# update edges value with naismith function
pd_itn_exp["weight"] = pd_itn_exp.apply(lambda x: naismith(x.distance, x.h), axis=1)

# aggregate weight by roadlink id
df_roadlink = pd.DataFrame(pd_itn_exp[["fid", "weight"]].groupby("fid").sum("weight")).reset_index()
df_roadlink = df_roadlink.merge(pd_itn, on="fid")

# digraph
itn_digraph = nx.DiGraph()

# for link in df_roadlink["fid"]:
#     print("link ", link)
#     link = str(link)
#     start_pt = df_roadlink.loc[df_roadlink["fid"] == link, "start"][0]
#     end_pt = df_roadlink.loc[df_roadlink["fid"] == link, "end"][0]
#     print("start ", start_pt, "end ", end_pt)
#     itn_digraph.add_edge(start_pt, end_pt, fid=link, weight=df_roadlink[link]["weight"])

for link in range(len(df_roadlink["fid"])):
    fid = df_roadlink.loc[link, "fid"]
    start_pt = df_roadlink.loc[link, "start"]
    end_pt = df_roadlink.loc[link, "end"]
    weight = df_roadlink.loc[link, "weight"]
    itn_digraph.add_edge(start_pt, end_pt, fid=link, weight=weight)

# nx.draw(itn_digraph, node_size=1)


# Shortest path within the digraph
path = nx.dijkstra_path(itn_digraph, source="osgb4000000026141631", target="osgb4000000026126418", weight="weight")
path


nodes = gpd.read_file("/Users/mariebourel/Documents/Fac/Master 2022_2023/UCL/cours/CEGE0096 - Geospatial Programming/2nd Assignment/Material/roads/nodes.shp")
pt = nodes.merge(pd.DataFrame(path), right_on=0, left_on="fid")
pt = pt.rename(columns={0: "pathnod"})

pt.to_file("path.json", driver="GeoJSON")