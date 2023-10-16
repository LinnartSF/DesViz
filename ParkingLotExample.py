import simpy
import random

# modeling framework
class ParkingLot:

    env         :simpy.Environment
    capacity    :int
    spots       :simpy.resources.container.Container

    def __init__(self, 
        
        env :simpy.Environment, 
        capacity :int
        ):
        
        """ constructor """
        
        self.env = env
        self.capacity = capacity
        self.spots = simpy.resources.container.Container(env, capacity, init=capacity)
    
    def car_arrival(self,
        car_id :int
        ) -> None:
        """ 
    
        implement simpy process; 
        models car arrivals in the parking lot, occupying a slot for a randomly distributed duration
    
        """
    
        print(f"Car {car_id} arrives at {self.env.now}")
    
        yield self.spots.get(1)
        
        print(f"Car {car_id} parks at {self.env.now}")
        
        yield self.env.timeout(random.randint(1, 5))
        
        print(f"Car {car_id} leaves at {self.env.now}")
        
        yield self.spots.put(1)
    
    def main(self,
            runtime :int,
            interarrivaltime_min :int,
            interarrivaltime_max :int
            ) -> None:
        
        """ implements simpy process for main parking lot simulation run """
        
        for car in range(1, runtime+1):

            t = random.randint(interarrivaltime_min, interarrivaltime_max)

            yield self.env.timeout(t)

            self.env.process(self.car_arrival(car))


# setup model 
env = simpy.Environment()
parking_lot = ParkingLot(env, capacity=10)

# setup simulation run itself
env.process(parking_lot.main(runtime=10, interarrivaltime_min= 1, interarrivaltime_max=5))

# run the model
env.run()
