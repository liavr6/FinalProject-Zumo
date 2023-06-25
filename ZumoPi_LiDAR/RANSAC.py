import math
import random

# get degrees

def angle_from_y_axis(m):
	"""
	Computes the angle (in degrees) between a line with slope m and the y-axis.
	"""
	return 90 + math.degrees(math.atan(m))

# distance from wall

def distance_to_line(point, m, b):
	"""
	Computes the perpendicular distance between a point and a line in the form y = mx + b.
	"""
	x, y = point
	distance = abs(y - (m*x + b)) / math.sqrt(1 + m**2)
	return distance

def ransac(points, iterations, threshold):
	"""
	The "ransac" function estimates the parameters of a line that best fits observed data by using the RANSAC algorithm.
	"""
	best_m, best_b, best_count = 0, 0, 0
	for i in range(iterations):
		p1, p2 = random.sample(points, 2)
		m = (p2[1] - p1[1]) / (p2[0] - p1[0])
		b = p1[1] - m * p1[0]
		count = 0
		for p in points:
			if abs(p[1] - m * p[0] - b) < threshold:
				count += 1
		if count > best_count:
			best_m, best_b, best_count = m, b, count
	return best_m, best_b 

def polar_to_cartesian(polar_coords):
	"""
	The function takes a list of polar coordinates and returns their corresponding Cartesian coordinates using the conversion equations.
	"""
	cartesian_coords = []
	for polar_coord in polar_coords:
		radius, heading = polar_coord
		x = radius * math.cos(math.radians(heading))
		y = radius * math.sin(math.radians(heading))
		cartesian_coords.append((x, y))
	return cartesian_coords 