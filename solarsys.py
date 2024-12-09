import turtle
from math import *
import random
import time

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
sun.shapesize(2.7) 
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

# Create planets
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
        self.label = turtle.Turtle(visible=False)
        self.label.hideturtle()
        self.label.penup()
        self.label.color("white")

    def move(self):
        x = self.radius * cos(self.angle)
        y = self.radius * sin(self.angle)
        self.goto(sun.xcor() + x, sun.ycor() + y)
        self.angle += self.speed
        if self.label.isvisible():
            self.label.clear()
            self.label.goto(self.xcor(), self.ycor() + 15)
            self.label.write(self.name, align="center", font=("Arial", 10, "bold"))
            
# Hover detection function
def check_hover():
    # Get cursor position in the window's coordinate system
    mouse_x = screen.cv.winfo_pointerx() - screen.cv.winfo_rootx() - screen.window_width() // 2
    mouse_y = screen.window_height() // 2 - (screen.cv.winfo_pointery() - screen.cv.winfo_rooty())

    for planet in myList:
        if planet.distance(mouse_x, mouse_y) < 20:
            if not planet.label.isvisible():
                planet.label.showturtle()
                planet.label.clear()
                planet.label.goto(planet.xcor(), planet.ycor() + 15)
                planet.label.write(planet.name, align="center", font=("Arial", 10, "bold"))
        else:
            if planet.label.isvisible():
                planet.label.hideturtle()
                planet.label.clear()

    # Schedule the next check
    screen.ontimer(check_hover, 100)


details_turtle = turtle.Turtle()
details_turtle.hideturtle()
details_turtle.penup()
details_turtle.color("white")

def show_planet_details(planet):
    details_turtle.clear()

    # Move details popup to the bottom-right corner
    popup_x = screen.window_width() // 2 - 270
    popup_y = -screen.window_height() // 2 + 50
    details_turtle.goto(popup_x, popup_y)
    
    # Draw a background rectangle for the popup
    details_turtle.fillcolor("white")
    details_turtle.begin_fill()
    for _ in range(2):
        details_turtle.forward(240)
        details_turtle.left(90)
        details_turtle.forward(120)
        details_turtle.left(90)
    details_turtle.end_fill()

    # Add the planet's "image" as a small circle
    details_turtle.penup()
    details_turtle.goto(popup_x + 30, popup_y + 70)
    details_turtle.shape("circle")
    details_turtle.shapesize(2)
    details_turtle.color(planet.c)
    details_turtle.stamp()

    # Write the planet details
    details_turtle.penup()
    details_turtle.goto(popup_x + 80, popup_y+20)
    details_turtle.color("black")  # Change font color to black
    details_text = (
        f"Planet: {planet.name}\n"
        f"Orbit Radius: {planet.radius} units\n"
        f"Color: {planet.c}\n"
        f"Orbital Speed: {planet.speed:.4f}"
    )
    details_turtle.write(details_text, align="left", font=("Arial", 12, "normal"))

# Function to clear the details popup
def clear_details(x, y):
    details_turtle.clear()

# Bind the clear functionality to a click anywhere on the screen
screen.onclick(clear_details)

# Function to detect planet click
def detect_planet_click(x, y):
    for planet in myList:
        if planet.distance(x, y) < 20:  # Check if clicked near a planet
            show_planet_details(planet)
            screen.ontimer(details_turtle.clear, 5000) # Clear the details popup after 5sec if no click is done.
            break
    else:
        clear_details(x, y)  # Clear details if no planet is clicked

# Bind the updated click event
screen.onclick(detect_planet_click)

        
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
        self.shapesize(0.2) 
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



# Create planets
mercury = Planet("Mercury", 50, "grey", 0.005, 0.5)
venus = Planet("Venus", 90, "orange", 0.003, 0.8)
earth = Planet("Earth", 130, "blue", 0.001, 1)
mars = Planet("Mars", 160, "red", 0.0007, 0.6)
jupiter = Planet("Jupiter", 240, "brown", 0.002, 1.8)
saturn = Planet("Saturn", 290, "pink", 0.0018, 1.5)
uranus = Planet("Uranus", 340, "light blue", 0.0016, 1.2)
neptune = Planet("Neptune", 370, "purple", 0.0005, 1.1)

myList = [mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]

# Bind hover functionality
check_hover()

# Create Kuiper Belt objects
kuiper_belt = []
for _ in range(200):
    radius = random.uniform(400, 450)  # Adjusted range for a smaller belt
    kbo = KuiperBeltObject(radius)
    kuiper_belt.append(kbo)

# Create Asteroid Belt objects
asteroid_belt = []
for _ in range(200):  # 100 objects in the Asteroid Belt
    radius = random.uniform(180, 190)  # Random distance between Mars and Jupiter
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
        asteroid.move()
    saturn_rings.move()
