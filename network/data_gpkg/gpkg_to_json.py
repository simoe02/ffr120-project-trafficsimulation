# Code for converting gpkg data from Trafikverkete to a JSON of road segments

import geopandas as gpd
import json

gdf = gpd.read_file("network/data_gpkg/data.gpkg", layer="NVDB_DK_O_88_Vagtrafiknat")
car_network_gpf = gdf[gdf.Nattyp == "bilnät"]

print(car_network_gpf)

segments = []

for _, row in car_network_gpf.iterrows():
    geom = row.geometry

    # handle multilinestrings
    if geom.geom_type == "MultiLineString":
        lines = geom.geoms
    else:
        lines = [geom]

    for line in lines:
        # Extract start and end coordinates (only x, y)
        start_x, start_y = line.coords[0][:2]
        end_x, end_y     = line.coords[-1][:2]

        segments.append({
            "segment_id": row["ELEMENT_ID"],
            "length": float(row["EXTENT_LENGTH"]),
            "start": [int(start_x), int(start_y)],
            "end":   [int(end_x), int(end_y)],
        })

# Save to JSON
with open("network/road_data_gkpg/road_segments_clipped.json", "w") as file:
    json.dump(segments, file, indent=2)