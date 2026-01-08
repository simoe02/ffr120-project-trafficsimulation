from network.network import RoadNetwork
from driver_behavior.router import AstarRouter
from simulation import TrafficSimulation
# from visualizer import TrafficVisualizer


# def run_with_visualisation(filename: str, num_vehicles: int, dt: float = 0.016) -> None:
#     network = RoadNetwork()
#     network.init_from_json(f"network/data_gpkg/{filename}.json")

#     router = AstarRouter(network)
#     simulation = TrafficSimulation(network, router)

#     simulation.spawn_vehicle(num_vehicles)

#     vis = TrafficVisualizer(simulation, dt)
#     vis.run()
    
def run_simulation(
        network_filename: str, 
        num_vehicles: int, 
        dt: float, 
        T: float, 
        use_dynamic_spawning: bool, 
        saved_data_dirname: str,
        closed_roads_frac: float = 0,
        clock_speed: int = 1
    ) -> None:
    
    print("        Initializing...")
    
    network = RoadNetwork(closed_roads_frac=closed_roads_frac)
    network.init_from_json(f"network/data_gpkg/{network_filename}.json")

    router = AstarRouter(network)
    simulation = TrafficSimulation(network, router, collect_data=True, dynamic_spawn_rate=use_dynamic_spawning, clock_speed=clock_speed, saved_data_dirname=saved_data_dirname)

    simulation.spawn_vehicle(num_vehicles)
    
    iterations = int(T / dt / clock_speed)
    
    for t_i in range(iterations):
        if t_i % 1000 == 0:
            t_h = t_i*dt/3600 * clock_speed
            print(f"        t = {t_h:.3} h, N = {len(simulation.vehicles)}")
        simulation.step(dt)
    
    simulation.collector.save_to_csv()


if __name__ == "__main__":
    NETWORK_FILENAME = "large"
    N_START = 500
    DELTA_TIME = 0.1
    CLOCK_SPEED = 1 # seconds per seconds (to avoid simulating a whole 24*3600 seconds)
    RUNS_PER_P = 1
    TOTAL_TIME = 72 * 3600
    
    # run_with_visualisation(NETWORK_FILENAME, N_START, dt=0.1)
    
    # percentages = [0.00, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10]
    percentages = [0.10]
    
    for p in percentages:
        
        print(f"p = {p}")
        
        for i in range(RUNS_PER_P):
            saved_data_filename = f"{p}_{i}_72h_real_time"
            
            print(f"   Run {i}:")
        
            run_simulation(NETWORK_FILENAME, N_START, DELTA_TIME, TOTAL_TIME, use_dynamic_spawning=True, closed_roads_frac=p, clock_speed=CLOCK_SPEED, saved_data_dirname=saved_data_filename)
    
