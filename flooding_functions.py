"""
    File name: flooding_functions.py
    Description: For CEGE0096: Flooding Emergency Planning - classes used in main.py script
    Author: Falcon Team
    Date created: 10/12/2022
    Date last modified: 23/12/2022
    Python Version: 3.8
    Virtual env: geospatial
"""


# Define the time between nodes based on Naismith's rule
def naismith(distance, elevation): # https://medium.com/@sunside/naismith-aitken-langmuir-tranter-and-tobler-modeling-hiking-speed-4ff3937e6898
    """
    :param distance: meters between points
    :param elevation: difference in elevation between points
    :return: time to go from one point to the other
    """
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

