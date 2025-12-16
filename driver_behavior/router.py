from dataclasses import dataclass
from abc import abstractmethod
import heapq

from network.network import Road, Intersection, RoadNetwork

@dataclass(frozen=True)
class AStarEntry:
    """
    Priority queue entry. For use in A star graph search algorithms.
    """
    node: Intersection
    last_road: Road | None
    back_pointer: None # CHANGE FOR PYPY: back_pointer: Entry | None
    cost_to_here: float
    cost_to_goal_estimate: float

    def __lt__(self, other) -> bool: # CHANGE FOR PYPY: other: Entry
        return self.cost_to_here + self.cost_to_goal_estimate < other.cost_to_here + other.cost_to_goal_estimate


class PriorityQueue:
    """
    An implementation of priority queues using the heapq library. For use in graph search algorithms.
    """
    def __init__(self):
        self.heap: list[AStarEntry] = []
    
    def is_empty(self) -> bool:
        """Returns true if the priority queue is empty."""
        return len(self.heap) == 0

    def add(self, entry: AStarEntry):
        """Adds e to the priority queue."""
        heapq.heappush(self.heap, entry)

    def remove_min(self) -> AStarEntry:
        """
        Removes and returns the minimum element.
        Raises an IndexError if the priority queue is empty.
        """
        return heapq.heappop(self.heap)


@dataclass
class Route:
    roads: list[Road]
    cost_est: float
    

class Router:
    def __init__(self, graph: RoadNetwork):
        self.graph = graph

    @abstractmethod
    def find_route(self, start: Intersection, dest: Intersection, closed_roads: set = set()) -> Route:
        """
        Searches for a route in road network from start to dest.
        Returns a Route() if found.
        """
        
    def extract_path(self, entry: AStarEntry) -> list[Road]:
        """
        Extracts the path from the start to the current priority queue entry.
        """
        path = []

        while entry.last_road is not None:
            path.append(entry.last_road)
            
            if entry.back_pointer is not None: # to avoid type errors (entry.backpointer will never be None)
                entry = entry.back_pointer

        return path[::-1]


class AstarRouter(Router):
    """
    Router using A*-algorithm for finding shortest route to dest.
    """
    def find_route(self, start: Intersection, dest: Intersection, closed_roads: set = set()) -> Route | None:
        
        iterations = 0
        pqueue = PriorityQueue()
        visited = set()
        
        # Add first Entry to pqueue
        pqueue.add(AStarEntry(start, None, None, 0, self.graph.estimate_cost(start, dest)))
        
        while not pqueue.is_empty():
            iterations += 1
            entry = pqueue.remove_min()
            
            # Check if node is visited
            if entry.node in visited:
                continue
            visited.add(entry.node)

            # Return final route if current node is goal
            if entry.node == dest:
                return Route(self.extract_path(entry), entry.cost_to_here)

            # Add outgoing roads to pqueue
            for road in self.graph.adjacency_list[entry.node.id]:
                if (road.end not in visited) and (road.id not in closed_roads):
                    pqueue.add(AStarEntry(
                        road.end, 
                        road, 
                        entry, 
                        entry.cost_to_here+road.get_cost(), 
                        self.graph.estimate_cost(road.end, dest)
                        ))
                    
        return None
        
