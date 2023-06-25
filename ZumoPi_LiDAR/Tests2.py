import matplotlib.pyplot as plt
import numpy as np
import math
from Tests import *

def cartesian_to_polar(coordinates):
    polar_coordinates = []
    for x, y in coordinates:
        r = math.sqrt(x**2 + y**2)
        theta = math.atan2(y, x)
        polar_coordinates.append((r, theta))
    return polar_coordinates

def plot_polar_coordinates(polar_coordinates):
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='polar')
    ax.set_ylim([0, np.amax(polar_coordinates, axis=0)[0]])
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    for r, theta in polar_coordinates:
            ax.plot(theta, r, 'bo')
    plt.show()

import math

def generate_points_on_circle(radius, num_points):
    points = []
    for i in range(num_points):
        theta = i * (2 * math.pi / num_points)
        x = radius * math.cos(theta)
        y = radius * math.sin(theta)
        points.append((x, y))
    return points





# points = generate_points_on_circle(10, 20)

# points = [(-5, 30), (-4, 25), (-3, 20), (-2, 15), (-1, 10), (0, 5), (1, 0), (2, -5), (3, -10), (4, -15), (5, -20)] 

# points = linear_equation_to_polar_coordinates(2, 0)

# y = 2x
# points = [(0.0, 0.0), (2.23606797749979, 1.1071487177940904), (4.47213595499958, 1.1071487177940904), (6.708203932499369, 1.1071487177940904), (8.94427190999916, 1.1071487177940904), (11.180339887498949, 1.1071487177940904), (13.416407864998739, 1.1071487177940904), (15.652475842498528, 1.1071487177940904), (17.888543819998318, 1.1071487177940904), (20.124611797498107, 1.1071487177940904)] 

# y = -2x
#points = [(0.0, 0.0), (2.23606797749979, -2.0344439357957027), (4.47213595499958, -2.0344439357957027), (6.708203932499369, -2.0344439357957027), (8.94427190999916, -2.0344439357957027), (11.180339887498949, -2.0344439357957027), (13.416407864998739, -2.0344439357957027), (15.652475842498528, -2.0344439357957027), (17.888543819998318, -2.0344439357957027), (20.124611797498107, -2.0344439357957027)] 

#print(points)

#polar_coordinates = cartesian_to_polar(points)

#polar_coordinates = [(1, 0.5), (2, 1.2), (3, 2.5), (4, 4.7), (2.5, 5.9)]
#plot_polar_coordinates(polar_coordinates) 
