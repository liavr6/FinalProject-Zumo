import random
import numpy as np

def ransac_line_fit_cartesian(x, y, threshold, max_iterations):
    best_model = None
    best_inliers = []
    for i in range(max_iterations):
        # Randomly select two points to fit the line
        sample_indices = random.sample(range(len(x)), 2)
        x1 = x[sample_indices[0]]
        x2 = x[sample_indices[1]]
        y1 = y[sample_indices[0]]
        y2 = y[sample_indices[1]]
        # x1, x2 = x[sample_indices]
        # y1, y2 = y[sample_indices]

        # Calculate the parameters of the line (y = mx + b)
        m = (y2 - y1) / (x2 - x1)
        b = y1 - m * x1

        # Find the inliers within the threshold
        inliers = []
        for j in range(len(x)):
            if abs(y[j] - (m * x[j] + b)) < threshold:
                inliers.append(j)

        # If this model has more inliers than the current best model, update the best model
        if len(inliers) > len(best_inliers):
            best_inliers = inliers
            best_model = (m, b)

    # Fit the best model to all the inliers
    m, b = best_model
    inlier_x = [x[i] for i in best_inliers]
    inlier_y = [y[i] for i in best_inliers]
    A = np.vstack([inlier_x, np.ones(len(inlier_x))]).T
    m, b = np.linalg.lstsq(A, inlier_y, rcond=None)[0]

    return m, b 

def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)

def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y) 
