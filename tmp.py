import math

# 1. Abstraction: Creating an abstract base class
class Shape:
    """Abstract base class for all shapes."""

    def area(self):
        """Abstract method to calculate area."""
        pass

    def display(self):
        """Abstract method to display shape info."""
        pass

# 2. Inheritance: Subclasses inheriting from Shape class

class Circle(Shape):
    # constructor
    def __init__(self, radius):
        self.__radius = radius  # Encapsulation: Private attribute

    def area(self):
        """Calculates area of the circle."""
        return math.pi * self.__radius ** 2

    def display(self):
        """Displays circle info."""
        print(f"Circle: Radius = {self.__radius}, Area = {self.area():.2f}")

class Rectangle(Shape):
    def __init__(self, width, height):
        self.__width = width  # Encapsulation
        self.__height = height  # Encapsulation

    def area(self):
        """Calculates area of the rectangle."""
        return self.__width * self.__height

    def display(self):
        """Displays rectangle info."""
        print(f"Rectangle: Width = {self.__width}, Height = {self.__height}, Area = {self.area():.2f}")

class Triangle(Shape):
    def __init__(self, base, height):
        self.__base = base  # Encapsulation
        self.__height = height  # Encapsulation

    def area(self):
        """Calculates area of the triangle."""
        return 0.5 * self.__base * self.__height

    def display(self):
        """Displays triangle info."""
        print(f"Triangle: Base = {self.__base}, Height = {self.__height}, Area = {self.area():.2f}")

# 3. Polymorphism: Using common interface for different shapes

def print_area(shape):
    """A polymorphic function to print shape details."""
    shape.display()

# 4. Usage

# Create objects of different shapes
circle = Circle(5)
rectangle = Rectangle(10, 4)
triangle = Triangle(6, 3)

# Using polymorphism to print area for each shape
shapes = [circle, rectangle, triangle]
for shape in shapes:
    print_area(shape)
