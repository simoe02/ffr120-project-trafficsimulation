import osmnx as ox

graph = ox.graph_from_xml("network/road_data/linne.osm", simplify=True)

ox.plot_graph(graph)