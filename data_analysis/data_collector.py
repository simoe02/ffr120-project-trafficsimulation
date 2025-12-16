import pandas as pd
from datetime import datetime
import os

from driver_behavior.vehicle import Vehicle

class DataCollector:
    def __init__(self) -> None:
        self.time: list[float] = []
        
        self.avg_speed: list[float] = []
        self.number_of_vehicles: list[int] = []
        self.stopped_vehicles: list[int] = []
        self.completed_routes: list[dict] = []
        
        self.avg_delay: list[float] = []
        self.num_completed_routes: list[int] = []
        
        self.data: dict[str, list] = {
            "time": [], 
            "num_vehicles": [],
            "avg_speed": [],
            "stopped": [],
            "completed_routes": []
        }
        
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
            
        # self.time.append(time)
        # self.stopped_vehicles.append(stopped_vehicles)
        # self.avg_speed.append(avg_speed)
        # self.number_of_vehicles.append(len(vehicles))
        # self.num_completed_routes.append(len(self.completed_routes))
    
    def add_completed_route(self, time: float, vehicle: Vehicle) -> None:
        self.completed_routes.append(
            {
                "time": time,
                "delay": vehicle.lifetime - vehicle.estimated_cost_to_dest,
                "route_replannings": vehicle.num_replannings
            }
        )
        
    def save_to_csv(self) -> None:
        data_df = pd.DataFrame(self.data)
        
        routes_df = pd.DataFrame(self.completed_routes)
    
        timestamp = datetime.now().strftime("%H%M%S")

        os.mkdir(f"data/sim_data/{timestamp}")

        data_df.to_csv(f"data/sim_data/{timestamp}/data.csv")
        routes_df.to_csv(f"data/sim_data/{timestamp}/route_data.csv")
        