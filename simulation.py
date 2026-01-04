import random
import matplotlib.pyplot as plt # Used in old code

from network.network import RoadNetwork

from driver_behavior.vehicle import Vehicle
from driver_behavior.router import Router
from data_analysis.data_collector import DataCollector


class TrafficSimulation:
    def __init__(self, 
            network: RoadNetwork, 
            router: Router, 
            collect_data: bool = False, 
            dynamic_spawn_rate: bool = False, 
            clock_speed: float = 1
        ) -> None:
        
        self.network: RoadNetwork = network
        self.router: Router = router
        self.total_time: float = 0 # Time in simulation
        self.time_of_day: float = 0
        self.clock_speed: float = clock_speed
        
        self.vehicles: list[Vehicle] = []
        self.vehicles_by_id: dict[int, Vehicle] = {}
        self._next_vehicle_id = 0 # For vehicle spawning
        
        self.collect_data = collect_data
        if self.collect_data:
            self.collector = DataCollector()
            
        self.num_out_of_bounds = 0
        
        self.dynamic_spawn_rate: bool = dynamic_spawn_rate
        
        # Spawn rate per hour during the whole day {second: veh/hour}
        self.spawn_rates = {
            0*3600:   2000,
            3*3600:   3500,
            5*3600:   9000,
            6*3600:  16000,
            7*3600:  26000,
            8*3600:  23000,
            9*3600:  10000,
            11*3600: 8000,
            13*3600: 7000,
            15*3600: 8000,
            16*3600: 25000,
            17*3600: 24000,
            18*3600: 16000,
            19*3600: 11000,
            21*3600: 7000,
            23*3600: 3000,
        }
        
    def step(self, dt: float) -> None:
        """
        One simulation step
        """
        self.total_time = (self.total_time + dt * self.clock_speed) 
        self.time_of_day = self.total_time % (24 * 3600)
        
        if self.dynamic_spawn_rate:
            self.maybe_spawn_vehicle(dt)
            
        for vehicle in self.vehicles:
            
            vehicle.update(dt)
            
            if vehicle.destination_reached == 1: # reached dest
                del self.vehicles_by_id[vehicle.id]
                self.vehicles.remove(vehicle)
                
                if not self.dynamic_spawn_rate:
                    self.spawn_vehicle(1)
                
                if self.collect_data:
                    self.collector.add_completed_route(self.total_time, vehicle)
                
            elif vehicle.destination_reached == -1: # did not reach dest (out of bouds)
                del self.vehicles_by_id[vehicle.id]
                self.vehicles.remove(vehicle)
                
                self.num_out_of_bounds += 1
                
                if not self.dynamic_spawn_rate:
                    self.spawn_vehicle(1)
        
        if self.collect_data:
            self.collector.log(self.total_time, self.vehicles)
            
    def get_spawn_rate(self, t) -> float:
        times = sorted(self.spawn_rates.keys())
        for i in range(len(times) - 1):
            
            if times[i] <= t < times[i+1]:
                t0, t1 = times[i], times[i+1]
                r0, r1 = self.spawn_rates[t0], self.spawn_rates[t1]
                return r0 + (r1 - r0) * (t - t0) / (t1 - t0)
            
        return self.spawn_rates[times[-1]]
    
    def maybe_spawn_vehicle(self, dt: float) -> None:
        rate_per_hour = self.get_spawn_rate(self.time_of_day)
        p = rate_per_hour * dt / 3600.0

        if random.random() < p:
            self.spawn_vehicle(1)
        
    def spawn_vehicle(self, num: int = 1) -> None:
        
        for n in range(num):

            vehicle_id = self._next_vehicle_id
            start = random.choice(self.network.intersections_by_id)
            dest = random.choice(self.network.intersections_by_id)

            vehicle = Vehicle(
                id=vehicle_id,
                start=start,
                dest=dest, 
                router=self.router
            )
            
            self.vehicles.append(vehicle)
            self.vehicles_by_id[vehicle_id] = vehicle
            
            self._next_vehicle_id += 1
       
    # Old slow code (do not use for large graphs) 
    def visualize(self, show_paths: bool = False, save: bool = False) -> None:
        """
        Visualization of road network using matplotlib. Only works on smaller networks (see: johanneberg.json). Not animated.
        """
        plt.figure(figsize=(10, 10))
        for intersection in self.network.intersections:
            plt.scatter(intersection.x, intersection.y, color="black", s=5)
            
        for road in self.network.roads:

            if not road.closed:
                plt.plot([road.start.x, road.end.x], [road.start.y, road.end.y], color="black", alpha=0.8)
            else: 
                plt.plot([road.start.x, road.end.x], [road.start.y, road.end.y], color="red", alpha=0.8)
            
        # Plot vehicles
        for vehicle in self.vehicles:
            plt.scatter(vehicle.current_road.start.x, vehicle.current_road.start.y, marker="s", color="red", s=75, zorder=2)
            plt.scatter(vehicle.destination.x, vehicle.destination.y, color="red", marker="v", s=75, zorder=2)
            
            if show_paths == True:
                if vehicle.planned_route is not None: # to avoid type errors (planned route will never be None)
                    for road in vehicle.planned_route.roads:
                        plt.plot([road.start.x, road.end.x], [road.start.y, road.end.y], color="red", linewidth=5, alpha=0.8)
        
        plt.axis("off")
        plt.tight_layout()
        if save == True:
            plt.savefig("images/grid.pdf")
        plt.show()
        
