# Save as rocket1.py
from math import *

class rocket1():
    # rocket1 simulates a rocket1 ship for a game,
    #  or a physics simulation.
    
    def __init__(self, x=0, y=0):
        # Each rocket1 has an (x,y) position.
        self.x = x
        self.y = y
        
    def move_rocket(self, x_increment=0, y_increment=1):
        # Move the rocket1 according to the paremeters given.
        #  Default behavior is to move the rocket1 up one unit.
        self.x += x_increment
        self.y += y_increment
        
    def get_distance(self, other_rocket):
        # Calculates the distance from this rocket1 to another rocket1,
        #  and returns that value.
        distance = sqrt((self.x-other_rocket.x)**2+(self.y-other_rocket.y)**2)
        return distance
    
    def __str__(self):
        return f"A rocket1 positioned at ({self.x},{self.y})"

    def __repr__(self):
        return f"rocket1({self.x},{self.y})"

    def __eq__(self, other):
        # Check equality by comparing x and y coordinates of two rockets.
        if isinstance(other, rocket1):
            return self.x == other.x and self.y == other.y
        return False
    
    
class Shuttle(rocket1):
    # Shuttle simulates a space shuttle, which is really
    #  just a reusable rocket1.
    
    def __init__(self, x=0, y=0, flights_completed=0):
        super().__init__(x, y)
        self.flights_completed = flights_completed

class CircleRocket(rocket1):

    @staticmethod
    def get_area(r):
        return pi * r ** 2

    @staticmethod
    def get_circumference(r):
        return 2 * pi * r

# Example usage:
r= rocket1()
a = CircleRocket(r)
print(a.get_area(23))
print(a.get_circumference(23))