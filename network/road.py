from dataclasses import dataclass, field
from .intersection import Intersection

import random as random

@dataclass
class Road:
    """
    A class for representing roads as (one-way) edges in a (directed) graph.
    """
    id: int
    start: Intersection
    end: Intersection
    length: float
    vehicles: list = field(default_factory=list) # list[Vehicle]
    
    speed_limit: float = 13.89 # 13.89m/s = 50km/h (Constant speed limit not realistic but thats the best i can do right now)
    closed: bool = False
    
    def get_cost(self):
        """
        Calculate cost (expected time) for road.
        """
        return self.length / self.speed_limit
    
