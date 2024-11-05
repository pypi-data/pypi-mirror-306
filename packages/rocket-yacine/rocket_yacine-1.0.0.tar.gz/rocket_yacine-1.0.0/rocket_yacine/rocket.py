from math import sqrt

class Rocket():
    # Rocket simulates a rocket ship for a game,
    #  or a physics simulation.
    
    def __init__(self, x=0, y=0):
        # Each rocket has an (x,y) position.
        self.x = x
        self.y = y
        
    def move_rocket(self, x_increment=0, y_increment=1):
        # Move the rocket according to the paremeters given.
        #  Default behavior is to move the rocket up one unit.
        self.x += x_increment
        self.y += y_increment
        
    def get_distance(self, other_rocket):
        # Calculates the distance from this rocket to another rocket,
        #  and returns that value.
        distance = sqrt((self.x-other_rocket.x)**2+(self.y-other_rocket.y)**2)
        return distance
    
    def __str__(self):
        return f"A Rocket positioned at ({self.x},{self.y})"

    def __repr__(self):
        return f"Rocket({self.x},{self.y})"

    def __eq__(self, other):
        if isinstance(other, Rocket):
            return self.x == other.x and self.y == other.y
        return False
    
class Shuttle(Rocket):
    # Shuttle simulates a space shuttle, which is really
    #  just a reusable rocket.
    
    def __init__(self, x=0, y=0, flights_completed=0):
        super().__init__(x, y)
        self.flights_completed = flights_completed
    def __str__(self):
        return f"Shuttle positioned at ({self.x}, {self.y}), Flights Completed: {self.flights_completed}"

    def __repr__(self):
        return f"Shuttle({self.x}, {self.y}, Flights Completed: {self.flights_completed})"
    def get_distance(self, other):
        return super().get_distance(other)
    
class circleRocket(Rocket):
    def __init__(self, x=0, y=0, r=0):
        super().__init__(x, y)
        self.r = r

    def get_area(self):
        return 3.14 * self.r * self.r

    def get_circumference(self):
        return 2 * 3.14 * self.r

circleRock =circleRocket(1,2,3) 

print(f"Area: {circleRock.get_area()}")
print(f"Circumference: {circleRock.get_circumference()}")