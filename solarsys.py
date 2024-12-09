import turtle
from math import *
import random
import time

# Create the screen
screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Interactive Solar System Simulation")
screen.setup(width=1.0, height=1.0)
screen.tracer(0)  # Disable automatic screen updates for smoother animation

# Create the Sun
sun = turtle.Turtle()
sun.shape("circle")
sun.color("yellow")
sun.shapesize(3)  # Enlarge the Sun
sun.penup()

# Add background stars
def create_starry_sky():
    star = turtle.Turtle()
    star.hideturtle()
    star.penup()
    star.color("white")
    for _ in range(100):  # Number of stars
        x = random.randint(-800, 800)
        y = random.randint(-600, 600)
        star.goto(x, y)
        star.dot(random.randint(2, 4))

create_starry_sky()

# Create labels for planets
def create_planet_label(planet):
    label = turtle.Turtle()
    label.hideturtle()
    label.penup()
    label.color("white")
    label.goto(planet.xcor(), planet.ycor() + 15)
    label.write(planet.name, align="center", font=("Arial", 10, "bold"))
    return label

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
        self.label = create_planet_label(self)

    def move(self):
        x = self.radius * cos(self.angle)
        y = self.radius * sin(self.angle)
        self.goto(sun.xcor() + x, sun.ycor() + y)
        self.angle += self.speed
        self.label.clear()
        self.label.goto(self.xcor(), self.ycor() + 15)
        self.label.write(self.name, align="center", font=("Arial", 10, "bold"))
        
class AsteroidBeltObject(turtle.Turtle):
    def __init__(self, radius, color="gray"):
        super().__init__(shape="circle")
        self.radius = radius
        self.angle = random.uniform(0, 2 * pi)  # Random initial angle
        self.color(color)
        self.shapesize(0.1)  # Make the asteroids smaller
        self.penup()
    
    def move(self):
        # Calculate the new position based on the radius and angle
        x = self.radius * cos(self.angle)
        y = self.radius * sin(self.angle)

        # Move the object
        self.goto(sun.xcor() + x, sun.ycor() + y)

        # Slowly adjust the angle to simulate orbit
        self.angle += random.uniform(0.002, 0.005)

class KuiperBeltObject(turtle.Turtle):
    def __init__(self, radius, color="white"):
        super().__init__(shape="circle")
        self.radius = radius
        self.angle = random.uniform(0, 2 * pi)
        self.color(color)
        self.shapesize(0.2)  # Make Kuiper Belt objects small
        self.penup()

    def move(self):
        x = self.radius * cos(self.angle)
        y = self.radius * sin(self.angle)
        self.goto(sun.xcor() + x, sun.ycor() + y)
        self.angle += random.uniform(0.001, 0.003)

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

def show_planet_details(planet):
    details_screen = turtle.Screen()
    details_screen.bgcolor("black")
    details_screen.title(f"{planet.name} Details")
    details_turtle = turtle.Turtle()
    details_turtle.hideturtle()
    details_turtle.color("white")
    details_turtle.penup()
    details_turtle.goto(0, 100)
    details_turtle.write(
        f"Name: {planet.name}\nRadius: {planet.radius} units\nColor: {planet.c}\nSpeed: {planet.speed:.3f}",
        align="center",
        font=("Arial", 16, "bold"),
    )
    details_screen.mainloop()

def on_click(x, y):
    for planet in myList:
        if planet.distance(x, y) < 20:
            show_planet_details(planet)

# Bind click event
screen.onclick(on_click)

# Create planets
mercury = Planet("Mercury", 40, "grey", 0.005, 0.5)
venus = Planet("Venus", 80, "orange", 0.003, 0.8)
earth = Planet("Earth", 100, "blue", 0.001, 1)
mars = Planet("Mars", 150, "red", 0.0007, 0.6)
jupiter = Planet("Jupiter", 200, "brown", 0.002, 2)
saturn = Planet("Saturn", 230, "pink", 0.0018, 1.5)
uranus = Planet("Uranus", 250, "light blue", 0.0016, 1.2)
neptune = Planet("Neptune", 280, "purple", 0.0005, 1.1)

myList = [mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]

# Create Kuiper Belt objects
kuiper_belt = []
for _ in range(50):
    radius = random.uniform(300, 400)
    kbo = KuiperBeltObject(radius)
    kuiper_belt.append(kbo)

# Create Asteroid Belt objects
asteroid_belt = []
for _ in range(100):  # 100 objects in the Asteroid Belt
    radius = random.uniform(160, 170)  # Random distance between Mars and Jupiter
    asteroid = AsteroidBeltObject(radius)
    asteroid_belt.append(asteroid)

# Create Saturn's rings
saturn_rings = Ring(saturn, [10, 15, 20], color="white")

# Main simulation loop
while True:
    screen.update()
    for planet in myList:
        planet.move()
    for kbo in kuiper_belt:
        kbo.move()
    for asteroid in asteroid_belt:
        asteroid.move()  # Move each asteroid
    saturn_rings.move()
