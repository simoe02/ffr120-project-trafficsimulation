from dataclasses import dataclass

@dataclass(frozen=True)
class Intersection:
    """
    A class for representing intersections as nodes in a graph.
    """
    id: int
    x: float
    y: float
    
    # Not used
    traffic_light: bool = False # Determines time at intersection
    
