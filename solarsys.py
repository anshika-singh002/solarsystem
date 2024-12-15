import turtle
from math import cos, sin, pi
import random

# Initialize the screen
screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Interactive Solar System Simulation")
screen.setup(width=1.0, height=1.0)
screen.tracer(0)

# Create the Sun
sun = turtle.Turtle()
sun.shape("circle")
sun.color("yellow")
sun.shapesize(3.0)
sun.penup()

# Create the starry sky
def create_starry_sky():
    star = turtle.Turtle(visible=False)
    star.penup()
    star.color("white")
    for _ in range(100):
        star.goto(random.randint(-800, 800), random.randint(-600, 600))
        star.dot(random.randint(2, 4))

create_starry_sky()

# Planet class
class Planet(turtle.Turtle):
    def __init__(self, name, radius, color, speed, size):
        super().__init__(shape="circle")
        self.name = name
        self.radius = radius
        self.color(color)
        self.speed = speed
        self.shapesize(size)
        self.penup()
        self.angle = random.uniform(0, 2 * pi)
        self.label = turtle.Turtle(visible=False)
        self.label.penup()
        self.label.color("white")
        self.moons = []

    def move(self):
        self.goto(sun.xcor() + self.radius * cos(self.angle), sun.ycor() + self.radius * sin(self.angle))
        self.angle += self.speed
        self.update_label()
        for moon in self.moons:
            moon.move(self.xcor(), self.ycor())

    def update_label(self):
        if self.label.isvisible():
            self.label.clear()
            self.label.goto(self.xcor(), self.ycor() + 15)
            self.label.write(self.name, align="center", font=("Arial", 10, "bold"))

class Moon(turtle.Turtle):
    def __init__(self, name, radius, color, speed, size):
        super().__init__(shape="circle")
        self.name = name
        self.radius = radius
        self.color(color)
        self.speed = speed
        self.shapesize(size)
        self.penup()
        self.angle = random.uniform(0, 2 * pi)

    def move(self, planet_x, planet_y):
        self.goto(planet_x + self.radius * cos(self.angle), planet_y + self.radius * sin(self.angle))
        self.angle += self.speed

# Handle hover detection
def check_hover():
    mouse_x = screen.cv.winfo_pointerx() - screen.cv.winfo_rootx() - screen.window_width() // 2
    mouse_y = screen.window_height() // 2 - (screen.cv.winfo_pointery() - screen.cv.winfo_rooty())
    for planet in planets:
        if planet.distance(mouse_x, mouse_y) < 20:
            planet.label.showturtle()
            planet.update_label()
        else:
            planet.label.hideturtle()
            planet.label.clear()
    screen.ontimer(check_hover, 100)

# Show planet details
def show_planet_details(planet):
    details.clear()
    popup_x, popup_y = screen.window_width() // 2 - 270, -screen.window_height() // 2 + 50
    details.goto(popup_x, popup_y)
    details.fillcolor("white")
    details.begin_fill()
    for _ in range(2):
        details.forward(240)
        details.left(90)
        details.forward(120)
        details.left(90)
    details.end_fill()
    details.goto(popup_x + 30, popup_y + 70)
    details.shape("circle")
    details.shapesize(2)
    details.color(planet.fillcolor())
    details.stamp()
    details.goto(popup_x + 80, popup_y + 20)
    details.color("black")
    details.write(f"Planet: {planet.name}\nOrbit Radius: {planet.radius} units\nColor: {planet.fillcolor()}\nOrbital Speed: {planet.speed:.4f}", 
                  align="left", font=("Arial", 12, "normal"))

def clear_details(*_):
    details.clear()

# Click detection
screen.onclick(clear_details)
def detect_planet_click(x, y):
    for planet in planets:
        if planet.distance(x, y) < 20:
            show_planet_details(planet)
            break
    else:
        clear_details()

screen.onclick(detect_planet_click)

# Asteroid and Kuiper Belt Object classes
class BeltObject(turtle.Turtle):
    def __init__(self, radius, color, size, speed_range):
        super().__init__(shape="circle")
        self.radius = radius
        self.angle = random.uniform(0, 2 * pi)
        self.color(color)
        self.shapesize(size)
        self.penup()
        self.speed_range = speed_range

    def move(self):
        self.goto(sun.xcor() + self.radius * cos(self.angle), sun.ycor() + self.radius * sin(self.angle))
        self.angle += random.uniform(*self.speed_range)

# Ring class
class Ring:
    def __init__(self, planet, radii, color="white"):
        self.planet = planet
        self.radii = radii
        self.color = color
        self.ring_turtles = [(turtle.Turtle(visible=False), radius) for radius in radii]
        for ring_turtle, _ in self.ring_turtles:
            ring_turtle.speed(0)
            ring_turtle.color(self.color)
            ring_turtle.penup()

    def move(self):
        planet_x, planet_y = self.planet.xcor(), self.planet.ycor()
        for ring_turtle, radius in self.ring_turtles:
            ring_turtle.clear()
            ring_turtle.goto(planet_x, planet_y - radius)
            ring_turtle.pendown()
            ring_turtle.circle(radius)
            ring_turtle.penup()

# Comet class

class Comet(turtle.Turtle):
    def __init__(self):
        super().__init__(shape="circle")
        self.color("white")
        self.shapesize(0.4)
        self.penup()
        self.speed = random.uniform(3, 6)
        self.angle = random.uniform(0, 2 * pi)
        self.life_span = random.randint(50, 100)
        self.goto(random.randint(-screen.window_width() // 2, screen.window_width() // 2), 
                  random.randint(-screen.window_height() // 2, screen.window_height() // 2))

    def move(self):
        dx = self.speed * cos(self.angle)
        dy = self.speed * sin(self.angle)
        self.setx(self.xcor() + dx)
        self.sety(self.ycor() + dy)
        self.life_span -= 1
        if self.life_span <= 0:
            self.hideturtle()
            comets.remove(self)

# Create planets
planets = [
    Planet("Mercury", 50, "grey", 0.005, 0.5),
    Planet("Venus", 90, "orange", 0.003, 0.8),
    Planet("Earth", 130, "blue", 0.001, 1),
    Planet("Mars", 160, "red", 0.0007, 0.6),
    Planet("Jupiter", 240, "brown", 0.002, 1.8),
    Planet("Saturn", 290, "pink", 0.0018, 1.5),
    Planet("Uranus", 340, "light blue", 0.0016, 1.2),
    Planet("Neptune", 370, "purple", 0.0005, 1.1)
]

# Add moons to planets
planets[2].moons.append(Moon("Moon", 15, "white", 0.01, 0.3))  # Earth's moon
planets[4].moons.append(Moon("Io", 25, "yellow", 0.005, 0.4))  # Jupiter's Io
planets[4].moons.append(Moon("Europa", 35, "white", 0.004, 0.35))  # Jupiter's Europa
planets[5].moons.append(Moon("Titan", 30, "gold", 0.004, 0.5))  # Saturn's Titan
planets[6].moons.append(Moon("Miranda", 20, "grey", 0.006, 0.3))  # Uranus's Miranda
planets[7].moons.append(Moon("Triton", 25, "light grey", 0.005, 0.4))  # Neptune's Triton

check_hover()

# Create belts and rings
kuiper_belt = [BeltObject(random.uniform(400, 450), "white", 0.2, (0.001, 0.003)) for _ in range(200)]
asteroid_belt = [BeltObject(random.uniform(180, 190), "gray", 0.1, (0.002, 0.005)) for _ in range(200)]
saturn_rings = Ring(planets[5], [10, 15, 20])

# Comets
comets = []
def spawn_comet():
    if random.random() < 0.2:
        comets.append(Comet())
    screen.ontimer(spawn_comet, 500)

spawn_comet()

# Main loop
details = turtle.Turtle(visible=False)
details.penup()
details.color("white")

while True:
    screen.update()
    for planet in planets:
        planet.move()
    for obj in kuiper_belt + asteroid_belt:
        obj.move()
    for comet in comets[:]:
        comet.move()
    saturn_rings.move()
