# Save this code in rocket.py
import math

class Rocket():
    # Rocket simulates a rocket ship for a game,
    #  or a physics simulation.

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def move_rocket(self, x_increment=0, y_increment=1):
        self.x += x_increment
        self.y += y_increment

    def get_distance(self, other_rocket):
        distance = math.sqrt((self.x - other_rocket.x) ** 2 + (self.y - other_rocket.y) ** 2)
        return distance

    def __str__(self):
        return f"A Rocket positioned at ({self.x}, {self.y})"

    def __repr__(self):
        return f"Rocket({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class Shuttle(Rocket):
    # Shuttle simulates a space shuttle, a reusable rocket.
    
    def __init__(self, x=0, y=0, flights_completed=0):
        super().__init__(x, y)
        self.flights_completed = flights_completed

    def __str__(self):
        return f"Shuttle at ({self.x}, {self.y}) with {self.flights_completed} flights completed"

class CircleRocket(Rocket):
    # CircleRocket simulates a rocket with a circular shape.

    def __init__(self, x=0, y=0, radius=1):
        super().__init__(x, y)
        self.radius = radius

    def get_area(self):
        # Calculate the area of the circular rocket
        return math.pi * self.radius ** 2

    def get_circumference(self):
        # Calculate the circumference of the circular rocket
        return 2 * math.pi * self.radius

    def __str__(self):
        return f"CircleRocket with radius {self.radius} at ({self.x}, {self.y})"
