# rocket.py
from math import sqrt, pi


class Rocket():
    def __init__(self, x=0, y=0):
        # Each rocket has an (x, y) position.
        self.x = x
        self.y = y

    def move_rocket(self, x_increment=0, y_increment=1):
        # Move the rocket according to the parameters given.
        # Default behavior is to move the rocket up one unit.
        self.x += x_increment
        self.y += y_increment

    def get_distance(self, other_rocket):
        # Calculates the distance from this rocket to another rocket,
        # and returns that value.
        root = (self.x - other_rocket.x) ** 2 + (self.y - other_rocket.y) ** 2
        distance = sqrt(root)
        return distance

    def __str__(self):
        return f"A Rocket positioned at ({self.x}, {self.y})"

    def __repr__(self):
        return f"Rocket({self.x}, {self.y})"

    def __eq__(self, other):
        # Object Equality Method
        if isinstance(other, Rocket):
            return self.x == other.x and self.y == other.y
        return False


class Shuttle(Rocket):
    # Shuttle simulates a space shuttle, which is really
    # just a reusable rocket.

    def __init__(self, x=0, y=0, flights_completed=0):
        super().__init__(x, y)
        self.flights_completed = flights_completed


class CircleRocket(Rocket):
    # CircleRocket models a rocket in the shape of a circle with radius r.

    def __init__(self, x=0, y=0, radius=1):
        super().__init__(x, y)
        self.radius = radius

    def get_area(self):
        # Calculate the area of the circle.
        return pi * (self.radius ** 2)

    def get_circumference(self):
        # Calculate the circumference of the circle.
        return 2 * pi * self.radius
