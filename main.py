from network.network import RoadNetwork
from driver_behavior.router import AstarRouter
from simulation import TrafficSimulation
    
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
    network.init_from_json(f"network/road_data/{network_filename}.json")

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

def run_with_visualisation(filename: str, num_vehicles: int, dt: float = 0.01667, close_roads_frac: float = 0, use_dynamic_spawning: bool = True) -> None:
    from visualizer import TrafficVisualizer
    
    network = RoadNetwork()
    network.init_from_json(f"network/road_data/{filename}.json")

    router = AstarRouter(network)
    simulation = TrafficSimulation(network, router, dynamic_spawn_rate=True)

    simulation.spawn_vehicle(num_vehicles)

    vis = TrafficVisualizer(simulation, dt)
    vis.run()

if __name__ == "__main__":
    NETWORK_FILENAME = "large"
    N_START = 3000
    
    # Run with visualization
    DELTA_TIME = 0.01667 # 0.01667 s correspons to "real time" (since visualization run at 60 FPS)
    run_with_visualisation(NETWORK_FILENAME, N_START, DELTA_TIME, close_roads_frac=0)
    
    
    # Run without sim: (For much faster runtime use pypy as interpreter)
    
    # data_dirname = "sim_data"
    # p_close = 0
    # DELTA_TIME = 1
    # TOTAL_TIME = 72 * 3600

    # run_simulation(NETWORK_FILENAME, N_START, DELTA_TIME, TOTAL_TIME, use_dynamic_spawning=True, closed_roads_frac=p_close, saved_data_dirname=data_dirname)
    