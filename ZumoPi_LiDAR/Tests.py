
from Junk import *
from RANSAC import *

# dots = [(0,5), (1,10), (2,15), (3,20), (4,25), (5,30), (6,35), (7,40), (8,45), (9,50), (10,55), (11,60), (12,65), (13,70), (14,75), (15,80), (16,85), (17,90), (18,95), (19,100)]

# y = x
# dots = [(0,0), (1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7), (8,8), (9,9), (10,10)] 

# noisy_dots = [(x, y + random.uniform(-2, 2)) for x, y in dots]

# data = [(5,	0),
# 		(6.00333240792145,	88.0908475670036 / 180 * np.pi),
# 		(8.02246844805263,	85.710846671181 / 180 * np.pi),
# 		(10.0498756211209,	84.2894068625004 / 180 * np.pi),
# 		(12.0813906484312,	83.3455749539934 / 180 * np.pi),
# 		(15.1327459504216,	82.4053566314086 / 180 * np.pi)]

# data_x = [cart2pol(dot[0], dot[1])[0] for dot in dots]
# data_y = [cart2pol(dot[0], dot[1])[1] for dot in dots]

# print(data_x)
# print(data_y)

# data = list(zip(data_x, data_y))

# print(data)

# print(dots)

# x_coords = [dot[0] for dot in dots]
# y_coords = [dot[1] for dot in dots]

# print(ransac_line_fit_cartesian(x_coords, y_coords, 0.5, 20), angle_from_y_axis(ransac_line_fit_cartesian(x_coords, y_coords, 0.5, 20)[0]))


# points = polar_to_cartesian(linear_equation_to_polar_coordinates(5, 5))

# y = -5x - 5
# points = [(1, -10), (2, -15), (3, -20), (4, -25), (5, -30), (6, -35), (7, -40), (8, -45), (9, -50), (10, -55)]

# y = -3x + 9
points_y1 = [(-5, 24), (-4, 21), (-3, 18), (-2, 15), (-1, 12), (0, 9), (1, 6), (2, 3), (3, 0), (4, -3)]

# y = -22x
points_y2 = [(-5, 110), (-4, 88), (-3, 66), (-2, 44), (-1, 22), (0, 0), (1, -22), (2, -44), (3, -66), (4, -88)]

# y = 2x - 3
points_y3 = [(-5, -13), (-4, -11), (-3, -9), (-2, -7), (-1, -5), (0, -3), (1, -1), (2, 1), (3, 3), (4, 5)] 


#m, b = ransac(points_y1, iterations=100, threshold=2)
# print("Best fit line: y = {:.2f}x + {:.2f}".format(m, b)) 
#m, b = ransac(points_y2, iterations=100, threshold=2)
# print("Best fit line: y = {:.2f}x + {:.2f}".format(m, b)) 
#m, b = ransac(points_y3, iterations=100, threshold=2)

# m, b = ransac(points, iterations=100, threshold=2)
# print("Best fit line: y = {:.2f}x + {:.2f}".format(m, b)) 

# Create a list of polar coordinates representing the line y=-5x+5
points = []
for x in range(-10, 11):
    y = -69*x + 420
    r = math.sqrt(x**2 + y**2)
    h = math.degrees(math.atan2(y, x))
    points.append((r, h))

# # Add some noise to the points
for i in range(20):
    r = random.uniform(0, 5)
    h = random.uniform(0, 360)
    points.append((r, h))

#kaki = polar_to_cartesian(points)

#m, b = ransac(kaki, iterations=100, threshold=2)
# m, b = ransac(points, iterations=100, threshold=2)

# m, b = ransac(points, iterations=100, threshold=2)
#print("Best fit line: y = {:.2f}x + {:.2f}".format(m, b)) 

# points = linear_equation_to_polar_coordinates(m=-5, b=5)
# print(points)

# Run the RANSAC algorithm
# slope, y_intercept = ransac_polar_to_cartesian(points)

# Check that the result is close to y=-5x+5
# print(f"slope: {slope}, y_intercept: {y_intercept}") 
import matplotlib.pyplot as plt

def plot_lines(lines_data):
    plt.clf()
    plt.xlim([-5, 5])
    plt.ylim([-5, 5])
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Linear Lines Plot')
    plt.grid(True)

    for m, b in lines_data:
        x = [-b/m, (1-b)/m]
        y = [-5, 5]
        plt.plot(x, y, linewidth=2)
        plt.draw() 
        plt.pause(1)

