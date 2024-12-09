import turtle
from math import *
import random

# Create the screen
screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Interactive Solar System Simulation")
screen.setup(width=1.0, height=1.0)
screen.tracer(0)

# Create the Sun
sun = turtle.Turtle()
sun.shape("circle")
sun.color("yellow")
sun.shapesize(3)
sun.penup()

# Add background stars
def create_starry_sky():
    star = turtle.Turtle()
    star.hideturtle()
    star.penup()
    star.color("white")
    for _ in range(100):
        x = random.randint(-800, 800)
        y = random.randint(-600, 600)
        star.goto(x, y)
        star.dot(random.randint(2, 4))

create_starry_sky()

class Planet(turtle.Turtle):
    def __init__(self, name, radius, color, speed, size):
        super().__init__(shape="circle")
        self.name = name
        self.radius = radius
        self.c = color
        self.speed = speed
        self.shapesize(size)
        self.color(self.c)
        self.penup()
        self.angle = random.uniform(0, 2 * pi)
        self.label = self.create_label()

    def create_label(self):
        label = turtle.Turtle()
        label.hideturtle()
        label.penup()
        label.color("white")
        label.goto(self.xcor(), self.ycor() + 15)
        label.write(self.name, align="center", font=("Arial", 10, "bold"))
        return label

    def move(self):
        x = self.radius * cos(self.angle)
        y = self.radius * sin(self.angle)
        self.goto(sun.xcor() + x, sun.ycor() + y)
        self.angle += self.speed
        self.label.clear()
        self.label.goto(self.xcor(), self.ycor() + 15)
        self.label.write(self.name, align="center", font=("Arial", 10, "bold"))

class Ring:
    def __init__(self, planet, radii, color="white"):
        self.planet = planet
        self.radii = radii
        self.color = color
        self.ring_turtles = []

        for radius in radii:
            ring_turtle = turtle.Turtle()
            ring_turtle.hideturtle()
            ring_turtle.speed(0)
            ring_turtle.color(self.color)
            ring_turtle.penup()
            self.ring_turtles.append((ring_turtle, radius))

    def move(self):
        planet_x, planet_y = self.planet.xcor(), self.planet.ycor()
        for ring_turtle, radius in self.ring_turtles:
            ring_turtle.clear()
            ring_turtle.goto(planet_x, planet_y - radius)
            ring_turtle.pendown()
            ring_turtle.circle(radius)
            ring_turtle.penup()

class BeltObject(turtle.Turtle):
    def __init__(self, radius, color="gray", size=0.2, speed_range=(0.002, 0.005)):
        super().__init__(shape="circle")
        self.radius = radius
        self.angle = random.uniform(0, 2 * pi)
        self.color(color)
        self.shapesize(size)
        self.penup()
        self.speed = random.uniform(*speed_range)

    def move(self):
        x = self.radius * cos(self.angle)
        y = self.radius * sin(self.angle)
        self.goto(sun.xcor() + x, sun.ycor() + y)
        self.angle += self.speed

# Create planets
planets = [
    {"name": "Mercury", "radius": 40, "color": "grey", "speed": 0.005, "size": 0.5},
    {"name": "Venus", "radius": 80, "color": "orange", "speed": 0.003, "size": 0.8},
    {"name": "Earth", "radius": 100, "color": "blue", "speed": 0.001, "size": 1},
    {"name": "Mars", "radius": 150, "color": "red", "speed": 0.0007, "size": 0.6},
    {"name": "Jupiter", "radius": 180, "color": "brown", "speed": 0.002, "size": 2},
    {"name": "Saturn", "radius": 230, "color": "pink", "speed": 0.0018, "size": 1.5},
    {"name": "Uranus", "radius": 250, "color": "light blue", "speed": 0.0016, "size": 1.2},
    {"name": "Neptune", "radius": 280, "color": "purple", "speed": 0.0005, "size": 1.1},
]

planet_objects = []
for planet in planets:
    planet_obj = Planet(**planet)
    planet_objects.append(planet_obj)

# Create Saturn's rings
saturn = planet_objects[5]  # Saturn is the 6th planet in the list
saturn_rings = Ring(saturn, [10, 15, 20], color="white")

# Create asteroid belt (between Mars and Jupiter)
asteroid_belt = [BeltObject(radius=random.uniform(160, 180)) for _ in range(100)]

# Create Kuiper Belt (beyond Neptune)
kuiper_belt = [BeltObject(radius=random.uniform(300, 400)) for _ in range(50)]

# Main simulation loop
while True:
    screen.update()
    for planet in planet_objects:
        planet.move()
    saturn_rings.move()
    for asteroid in asteroid_belt:
        asteroid.move()
    for kbo in kuiper_belt:
        kbo.move()
