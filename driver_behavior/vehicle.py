import random
import math

from .router import Route, Router

from network.network import Road, Intersection


class Vehicle:
    """
    Class for simulating a vehicle on the road network as an independent agent. Each agent gets a random "aggression" level that determines parameters for the car followong logic.
    """
    def __init__(self, 
        id: int, 
        start: Intersection, 
        dest: Intersection,
        router: Router
        ) -> None:
        
        self.id: int = id
        self.router: Router = router
        
        while True:
            self.planned_route: Route | None = self.router.find_route(start, dest) # None/[] if it cant find route
            
            # Re-asign random start if router cant find route (not best solution but will have to do right now)
            if self.planned_route == None:
                start = random.choice(self.router.graph.intersections_by_id)
                dest = random.choice(self.router.graph.intersections_by_id)
            elif not self.planned_route.roads:
                start = random.choice(self.router.graph.intersections_by_id)
                dest = random.choice(self.router.graph.intersections_by_id)
            else:
                break
        
        self.num_replannings: int = 0

        self.destination: Intersection = dest
        self.estimated_cost_to_dest: float = self.planned_route.cost_est
        self.destination_reached: int = 0 # 0 if not reched dest yet, 1 if reached dest, -1 if out of bounds
        
        self.current_road: Road = self.planned_route.roads.pop(0)
        self.position_on_road: float = 0
        self.known_closed_roads_ids: set = set()
        
        self.current_road.vehicles.append(self)
        
        # Geographic positions for plotting
        self.x: float = self.current_road.start.x
        self.y: float = self.current_road.start.y
        
        self.speed: float = 0
        
        self.lifetime: float = 0
        
        self.length: float = 4.5
        
        # Driver attributes via a random agression parameter
        self.aggression = random.betavariate(2.5, 2.5)
        
        self.speed_limit_compiance = 0.85 + 0.3 * self.aggression
        self.acc_max = 1 + 3 * self.aggression
        self.brake_max = 3 + 4.0 * self.aggression
        self.time_headway = 3 - 2 * self.aggression # Time between vehicle in front
        self.tau = 4 - 2.5 * self.aggression # Speed adaptation time
        self.gamma = 0.4 + 0.4 * self.aggression # Speed difference sensitivity
    
    def update(self, dt: float) -> None:
        """
        Update vehicle one time step (dt). First update speed and pos. Then check if still on current road, if not decide which road to go to next.
        """
        self.lifetime += dt
        
        self.update_speed_pos(dt)
            
        # Check out of bounds (Buggy, fix later)
        if self.out_of_bounds() == True:
            self.destination_reached = -1
            return
            
        # Advance to next road (TODO: add check if next road congested)
        if self.position_on_road > self.current_road.length:
            
            # Add random intersection friction (traffic ligth, left turn, etc.). Right now very simple implementation.
            r = random.random()
            if 0.1 < r < 0.5:
                self.speed *= 0.7
            elif r < 0.1:
                self.speed *= 0.1
            
            if self.current_road.end == self.destination:
                self.destination_reached = 1
                return
            
            if self.planned_route is not None: # To avoid type error (planned route will never be None here)
                
                # "Fix" to a bug where the planned route was empty. But the bug doesnt seem to happen anymore.
                if not self.planned_route.roads:
                    print("Weird bug")
                    self.destination_reached = -1
                    return
                
                
                next_road = self.planned_route.roads[0]
                
                if next_road.closed == True:
                    self.known_closed_roads_ids.add(next_road.id)
                    self.replan_route()
                    
                else:
                    self.current_road.vehicles.remove(self)
                    self.current_road = self.planned_route.roads.pop(0)
                    self.current_road.vehicles.append(self)
                    self.position_on_road = 0
                    
    def update_speed_pos(self, dt) -> None:
        """
        Update speed and position of vehicle depending on if there is a vehicle in front. 
        Uses Full Velocity Difference model (FVDM) from M. Treiber and A. Kesting.
        """
        front_vehicle, distance = self.vehicle_in_front()
        
        v_desired = self.current_road.speed_limit * self.speed_limit_compiance
        
        if front_vehicle == None:
            self.speed += self.acc_max * dt
            
            if self.speed > v_desired:
                self.speed = v_desired
            
        # FVDM
        else:
            gap = max(0, distance - front_vehicle.length)
            min_gap = 2
            # d_gap = 5
    
            dv = self.speed - front_vehicle.speed

            opt_speed = max(0, min(v_desired, (gap-min_gap)/self.time_headway))
            
            # Smoother aternative but a bit too smooth
            # opt_speed = 0.5 * v_desired * (math.tanh((gap - min_gap) / d_gap) + 1.0)

            interaction = max(1.0, gap / (v_desired * self.time_headway))

            a = (opt_speed - self.speed) / self.tau - self.gamma * dv / interaction

            a = max(-self.brake_max, min(a, self.acc_max))

            self.speed = max(0.0, self.speed + a * dt)
        
        # Update absolute pos (for plotting and checking out of bounds)
        self.position_on_road += self.speed * dt
        dx = self.current_road.end.x - self.current_road.start.x
        dy = self.current_road.end.y - self.current_road.start.y

        t = self.position_on_road / self.current_road.length  # fraction along the road
        self.x = self.current_road.start.x + t * dx
        self.y = self.current_road.start.y + t * dy
                    
    def vehicle_in_front(self): # CHANGE FOR PYPY: -> tuple[Vehicle | None , float]
        """
        Checks if there is a vehicle in front of self on current road and calculates distance to it.
        """
        v_front = None
        d = math.inf
        
        for v in self.current_road.vehicles:
            if self.current_road.start == v.current_road.start: # Check if they are going the same way
                if self.position_on_road < v.position_on_road < d:
                    d = v.position_on_road - self.position_on_road
                    v_front = v

        return v_front, d        
    
    def replan_route(self) -> None:
        self.num_replannings += 1
        self.planned_route = self.router.find_route(self.current_road.end, self.destination, self.known_closed_roads_ids)
        
    def out_of_bounds(self) -> bool:
        if (
            (self.x > self.router.graph.xmax) or 
            (self.x < self.router.graph.xmin) or 
            (self.y > self.router.graph.ymax) or 
            (self.y < self.router.graph.ymin)
        ):
            return True
        else:
            return False
        
    def estimate_cost_to_goal(self, inter1: Intersection, inter2: Intersection) -> float:
        return self.router.graph.estimate_cost(inter1, inter2, self.current_road.speed_limit)
    
