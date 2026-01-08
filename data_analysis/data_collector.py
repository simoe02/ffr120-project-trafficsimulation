import pandas as pd
from datetime import datetime
import os

from driver_behavior.vehicle import Vehicle

class DataCollector:
    """
    Class for collecting data during simulation and store in two seperate .csv files, one containg data each time step and one with data on every completed route.
    """
    def __init__(self, dirname: str | None = None) -> None:
        
        self.dirname = dirname
        
        self.data: dict[str, list] = {
            "time": [], 
            "num_vehicles": [],
            "avg_speed": [],
            "stopped": [],
            "completed_routes": []
        }
        
        self.completed_routes: list[dict] = []
        
        if dirname == None:
            self.dirname = datetime.now().strftime("%H%M%S")

        if not os.path.isdir(f"data/sim_data/{dirname}"):
            os.mkdir(f"data/sim_data/{dirname}")
            
    def get_avg_speed_and_stopped(self, vehicle_list: list[Vehicle]) -> tuple[float, int]:
        avg_speed = 0
        stopped_vehicles = 0
        for v in vehicle_list:
            if v.speed < 0.1:
                stopped_vehicles += 1
                
            avg_speed += v.speed
            
        avg_speed = avg_speed / len(vehicle_list)
            
        return avg_speed, stopped_vehicles
        
    def log(self, t: float, vehicles: list[Vehicle]) -> None:
        
        avg_speed, stopped_vehicles = self.get_avg_speed_and_stopped(vehicles)
            
        self.data["time"].append(t)
        self.data["num_vehicles"].append(len(vehicles))
        self.data["avg_speed"].append(avg_speed)
        self.data["stopped"].append(stopped_vehicles)
        self.data["completed_routes"].append(len(self.completed_routes))
        
        # Save every 100000 steps to keep the simulation from eating up RAM
        if len(self.data["time"]) > 100000:
            self.save_to_csv()
    
    def add_completed_route(self, time: float, vehicle: Vehicle) -> None:
        self.completed_routes.append(
            {
                "time": time,
                "est_route_time": vehicle.estimated_cost_to_dest,
                "actual_route_time": vehicle.lifetime,
                "delay": vehicle.lifetime - vehicle.estimated_cost_to_dest,
                "route_replannings": vehicle.num_replannings
            }
        )
        
    def save_to_csv(self) -> None:
        """
        Saves currently stored data to csv and frees up space.
        """
        data_df = pd.DataFrame(self.data)
        routes_df = pd.DataFrame(self.completed_routes)

        data_csv_path = f"data/sim_data/{self.dirname}/data.csv"
        route_csv_path = f"data/sim_data/{self.dirname}/route_data.csv"

        data_df.to_csv(data_csv_path, mode="a", header=not os.path.exists(data_csv_path))
        routes_df.to_csv(route_csv_path, mode="a", header=not os.path.exists(route_csv_path))
        
        self.data: dict[str, list] = {
            "time": [], 
            "num_vehicles": [],
            "avg_speed": [],
            "stopped": [],
            "completed_routes": []
        }
        
        self.completed_routes: list[dict] = []