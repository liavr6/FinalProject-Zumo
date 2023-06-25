from Output_LiDAR import *
from time import sleep
import rclpy
from rclpy.node import Node
from RANSAC import *
import os 
import numpy as np
from Tests import *
from Tests2 import *
import threading
import Driver
from Plotter import Plotter

file_path = '/home/pi/Downloads/ZumoPi_LiDAR/plot.csv'  # Update with your file path


try:

    print('dont forget to upload the arduino...')

    os.system('ros2 run rplidar_ros rplidar_composition --ros-args -p serial_port:=/dev/ttyUSB0 -p frame_id:=lidar_link -p angle_compensate:=true -p scan_mode:=Boost &')

    scan_processor = ScanProcessor()
    rclpy.init()
    
    sleep(1)

    # global fwd_dist, right_dist, right_ang, state
    
    # fwd_dist = 10
    # right_dist = 0.1
    # right_ang = 0

    driver_thread = threading.Thread(target=Driver.LoopbackTest)
    driver_thread.start()

    # Create an instance of DistancePlotter
    plotter = Plotter(file_path)

    # Create and start the plotter thread
    plotter_thread = threading.Thread(target=plotter.plot)
    plotter_thread.start()

    while True:

        point=0,0
        walls, raw_meas = output_lidar(scan_processor)
        pl=[]
        # sleep(0.1)
        # os.system("clear")
        for i in range(len(walls)):
            #plot_polar_coordinates(walls[i])
            m, b = ransac(polar_to_cartesian(walls[i]), iterations=900, threshold=0.1)
            # print("Best fit line: y{} = {:.2f}x + {:.2f}".format(i,m, b)) 
            # print("Distance: "+ str(distance_to_line(point,m,b)))
            if i==2:
                Driver.right_dist = distance_to_line(point,m,b) 
                Driver.right_ang = np.rad2deg(np.arctan(m))
            if i==3:
                # Driver.fwd_dist = distance_to_line(point,m,b)
                Driver.fwd_dist = float(raw_meas[0][0])
               
            # print(f"angle {i} is: {np.rad2deg(np.arctan(m))}")
            # print(len(walls[i]))
            pl.append([m,b])
        #lines = [(1, 0), (-0.5, 0.25), (2, -1)]
        #plot_lines(pl) 
        
except KeyboardInterrupt:
    # Stop the plotter thread
    plotter.stop()
    plotter_thread.join()

    # Save the measurements to a CSV file
    plotter.save_measurements_to_csv()

    Driver.quit = True
    driver_thread.join()
    sleep(0.1)
    exit(-1)
