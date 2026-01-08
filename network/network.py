import json
import random

from .intersection import Intersection
from .road import Road

class RoadNetwork:
    """
    A class for representing a road network as a graph with nodes and edges. Inits from JSON file of 
    road segments or as a grid of size N (used mainly for prototyping).
    """
    def __init__(self,
            closed_roads_frac: float = 0
        ) -> None:
        # Lists if iterating over all intersections. Maybe memory inefficient to store these as well but it will have to do.
        self.intersections: list[Intersection] = []
        self.roads: list[Road] = []
        
        # Dicts for fast lookup
        self.intersections_by_id: dict[int, Intersection] = {} 
        self.roads_by_id: dict[int, Road] = {}
        
        self.closed_roads_frac: float = closed_roads_frac
        
        self.closed_roads_by_id: dict[int, Road] = {}
        self.roads_changed: bool = False
        
        self.adjacency_list: dict[int, list[Road]] = {}
        
        self.xmax = 0
        self.xmin = 0
        self.ymax = 0
        self.ymin = 0
        
    def init_from_json(self, filepath: str) -> None:
        """
        Initialize network from a JSON file of road segments. JSON file created with network/data_gpkg/gpkg_to_json.py.
        """
        with open(filepath, "r") as f:
            segments = json.load(f)
            
        next_inter_id = 0
        next_road_id = 0
        
        # Helper dict for keeping track fo which intersections have been added
        coords_to_inter_id = {}

        for seg in segments:
            start = tuple(seg["start"])   # (x, y)
            end   = tuple(seg["end"])     # (x, y)
            length = ((start[0]-end[0])**2 + (start[1]-end[1])**2)**0.5

            # Check if start already exists, else add it
            exists = start in coords_to_inter_id
            if exists == True:
                start_inter_id = coords_to_inter_id[start]
                start_inter = self.intersections_by_id[start_inter_id]
            else: 
                start_inter_id = next_inter_id
                coords_to_inter_id[start] = start_inter_id
                
                start_inter = Intersection(id=start_inter_id, x=start[0], y=start[1])
                self.add_intersection(start_inter)
                next_inter_id += 1
            
            # Check if end exists, else add it
            exists = end in coords_to_inter_id
            if exists == True:
                end_inter_id = coords_to_inter_id[end]
                end_inter = self.intersections_by_id[end_inter_id]
            else: 
                end_inter_id = next_inter_id
                coords_to_inter_id[end] = end_inter_id
                
                end_inter = Intersection(id=end_inter_id, x=end[0], y=end[1])
                self.add_intersection(end_inter)
                next_inter_id += 1
            
            # Add road (and check if start==end to avoid loops)
            if start_inter.id != end_inter.id:
                
                # Randomly close the road if specified
                if random.random() < self.closed_roads_frac:
                    closed = True
                else:
                    closed = False
                
                self.add_road(
                    Road(
                        id=next_road_id,
                        start=start_inter,
                        end=end_inter,
                        length=length, 
                        closed=closed
                    )
                )
                next_road_id += 1
                
                # Also add road the other way
                self.add_road(
                    Road(
                        id=next_road_id,
                        start=end_inter,
                        end=start_inter,
                        length=length,
                        closed=closed
                    )
                )
                next_road_id += 1
                
        self.set_bounds()

    def add_road(self, road: Road) -> None:
        """
        Adds road to the road network graph. Both to list and dict.
        """
        self.roads.append(road)
        self.roads_by_id[road.id] = road
        
        if road.closed == True:
            self.closed_roads_by_id[road.id] = road
        
        if road.start.id in self.adjacency_list:
            self.adjacency_list[road.start.id].append(road)
        else:
            self.adjacency_list[road.start.id] = [road]
        
    def add_intersection(self, intersection: Intersection) -> None:
        """
        Adds intersection to the road network graph. Both to list and dict.
        """
        self.intersections.append(intersection)
        self.intersections_by_id[intersection.id] = intersection
        
        if not intersection.id in self.adjacency_list:
            self.adjacency_list[intersection.id] = []
            
    def set_bounds(self) -> None:
        """
        Calculates the largest/smallest coordinates for use as bounds in the Vehicle class.
        """
        self.xmax = self.intersections[0].x
        self.xmin = self.intersections[0].x
        self.ymax = self.intersections[0].y
        self.ymin = self.intersections[0].y
        
        for inter in self.intersections[1:]:
            if inter.x > self.xmax:
                self.xmax = inter.x
            if inter.x < self.xmin:
                self.xmin = inter.x
            if inter.y > self.ymax:
                self.ymax = inter.y
            if inter.y < self.ymin:
                self.ymin = inter.y
        
    def estimate_cost(self, inter1: Intersection, inter2: Intersection, speed: float = 13.89) -> float:
        """
        (Under)estimates cost (time) between two intersections using euclidian distance and 
        speed (default 13.89m/s = 50km/h). Used in the A* algorithm.
        """
        x1 = inter1.x
        y1 = inter1.y
        x2 = inter2.x
        y2 = inter2.y
        return ((x1-x2)**2 + (y1-y2)**2)**0.5 / speed

    # Not used
    def disable_road(self, road_id: int) -> None:
        self.roads_by_id[road_id].closed = True
        self.closed_roads_by_id[road_id] = self.roads_by_id[road_id]
        
    # Not used
    def enable_road(self, road_id: int) -> None:
        self.roads_by_id[road_id].closed = False
        del self.closed_roads_by_id[road_id]
    
    # Old code for prototyping
    def init_grid_N(self, N: int) -> None:
        """
        Init road network as a simple NxN grid of intersection and roads.
        """
        inter_grid: list[list[Intersection | None]] = [[None for _ in range(N)] for _ in range(N)]
        inter_id = 0
        road_id = 0
        
        # add intersections
        for y in range(N):
            for x in range(N):
                inter = Intersection(
                    id=inter_id,
                    x=x,
                    y=y
                )
                self.add_intersection(inter)
                inter_grid[y][x] = inter
                inter_id += 1
                
        # Add horisontal roads
        for y in range(N):
            for x in range(N-1):
                start_inter = inter_grid[y][x]
                end_inter = inter_grid[y][x+1]
                
                if start_inter is not None and end_inter is not None: # To avoid type error
                    road1 = Road(
                        id=road_id,
                        start=start_inter,
                        end=end_inter,
                        length=1
                    )
                
                    self.add_road(road1)
                    road_id += 1
                    road2 = Road(
                        id=road_id,
                        start=end_inter,
                        end=start_inter,
                        length=1
                    )
                
                self.add_road(road2)
                road_id += 1
                
        # Add vertical roads
        for y in range(N-1):
            for x in range(N):
                start_inter = inter_grid[y][x]
                end_inter = inter_grid[y+1][x]
                if start_inter is not None and end_inter is not None: # to avoid type error
                    road1 = Road(
                        id=road_id,
                        start=start_inter,
                        end=end_inter,
                        length=1
                    )
                    
                    self.add_road(road1)
                    road_id += 1
                    
                    road2 = Road(
                        id=road_id,
                        start=end_inter,
                        end=start_inter,
                        length=1
                    )
                
                self.add_road(road2)
                road_id += 1
    


