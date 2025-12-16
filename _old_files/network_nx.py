import networkx as nx
import osmnx as ox
import matplotlib.pyplot as plt

from ..network.intersection import Intersection
from ..network.road import Road
from ..network.network import RoadNetwork

class RoadNetworkNX(RoadNetwork):
    """
    Class for representing a road network as a NetworkX Graph.
    """
    def __init__(self) -> None:
        self.graph = nx.DiGraph()
        
    def add_intersection(self, intersection: Intersection) -> None:
        self.graph.add_node(
            intersection.id,
            data=intersection
            )
        
    def add_road(self, road: Road) -> None:
        self.graph.add_edge(
            road.start.id,
            road.end.id,
            data=road
        )
        
    def init_from_osm(self, filepath: str) -> None:
        raise NotImplementedError()
    
    def neigbour_ids(self, node_id: int) -> list[int]:
        return list(self.graph.neighbors(node_id))
    
    def disable_road(self, start_id: int, end_id: int) -> None:
        self.graph[start_id, end_id]["data"].closed = True

    def visualize(self, save: bool) -> None:
        pos = {n: (self.graph.nodes[n]["data"].x, self.graph.nodes[n]["data"].y) for n in self.graph.nodes}
        nx.draw(self.graph, pos, with_labels=False, node_size=10, node_color='skyblue', arrowsize=10)
        if save == True:
            plt.savefig("images/grid_nx.pdf")
        plt.show()

    