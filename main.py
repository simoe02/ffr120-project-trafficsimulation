from network.network import RoadNetwork
from driver_behavior.router import AstarRouter
from simulation import TrafficSimulation
from visualizer import TrafficVisualizer


def run_with_visualisation(filename: str, num_vehicles: int, dt: float = 0.016) -> None:
    network = RoadNetwork()
    network.init_from_json(f"network/data_gpkg/{filename}.json")

    router = AstarRouter(network)
    simulation = TrafficSimulation(network, router)

    simulation.spawn_vehicle(num_vehicles)

    vis = TrafficVisualizer(simulation, dt)
    vis.run()
    
def run_simulation(
        filename: str, 
        num_vehicles: int, 
        dt: float, 
        T: float, 
        use_dynamic_spawning: bool, 
        closed_roads_frac: float = 0,
        clock_speed: int = 1
    ) -> None:
    
    network = RoadNetwork(closed_roads_frac=closed_roads_frac)
    network.init_from_json(f"network/data_gpkg/{filename}.json")

    router = AstarRouter(network)
    simulation = TrafficSimulation(network, router, collect_data=True, dynamic_spawn_rate=use_dynamic_spawning, clock_speed=clock_speed)

    simulation.spawn_vehicle(num_vehicles)
    
    iterations = int(T / dt / clock_speed)
    
    print("Warmup run...")
    simulation.collect_data = False
    for t_i in range(iterations):
        if t_i % 1000 == 0:
            t_h = t_i*dt/3600 * clock_speed
            print(f"t = {t_h:.3} h, N = {len(simulation.vehicles)}")
        simulation.step(dt)
    
    print("Real run")
    simulation.collect_data = True
    simulation.time = 0
    for t_i in range(iterations):
        if t_i % 1000 == 0:
            t_h = t_i*dt/3600 * clock_speed
            print(f"t = {t_h:.3} h, N = {len(simulation.vehicles)}")
        simulation.step(dt)
    
    simulation.collector.save_to_csv()


if __name__ == "__main__":
    NETWORK_FILENAME = "large"
    N_START = 7000
    DELTA_TIME = 0.1
    CLOCK_SPEED = 6 # seconds per seconds (to avoid simulating a whole 24*3600 seconds)
    
    run_with_visualisation(NETWORK_FILENAME, N_START, dt=0.1)
    
    # run_simulation(NETWORK_FILENAME, N_START, DELTA_TIME, 24*3600, use_dynamic_spawning=True, closed_roads_frac=0.1, clock_speed=CLOCK_SPEED)
    
