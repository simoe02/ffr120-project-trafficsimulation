# Code for picking a smaller rectangular window of the road network using lat/long coords

import json
from pyproj import Transformer

def latlong_to_sweref(latlong):
    """
    Function for converting latitude/longitude coordinates to the SWEREF system.
    """
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:3006", always_xy=True)
    
    lat, long = latlong
    
    sweref = transformer.transform(long, lat)
    return sweref
    

def create_sub_data(filename, xmin, ymin, xmax, ymax):
    with open("network/road_data_gpkg/whole_gbg.json", "r") as file:
        data = json.load(file)
    
    new_data = []

    for row in data:
        xstart = row["start"][0]
        ystart = row["start"][1]
        
        xend = row["end"][0]
        yend = row["end"][1]
        
        if xstart > xmax or xstart < xmin:
            continue
        elif ystart > ymax or ystart < ymin:
            continue
        elif xend > xmax or xend < xmin:
            continue
        elif yend > ymax or yend < ymin:
            continue
        else:
            new_data.append(row)
            
    with open(f"network/road_data_gpkg/{filename}.json", "w") as file:
        json.dump(new_data, file, indent=2)
    
if __name__ == "__main__":
    # Take latlong coords from map
    latlong_min = (57.683439, 11.966037)
    latlong_max = (57.696860, 11.982434)
    
    xmin, ymin = latlong_to_sweref(latlong_min)
    xmax, ymax = latlong_to_sweref(latlong_max)

    new_filename = "data_small"
    
    create_sub_data(new_filename, xmin, ymin, xmax, ymax)
    