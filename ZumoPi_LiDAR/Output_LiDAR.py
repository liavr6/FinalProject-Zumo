from rplidar import RPLidar
from RANSAC import *
from listener import *
from Tests import *
"""
	!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	maybe put the "try", "while", "except" in a different thread
"""

def output_lidar(scan_processor):
	lidar = RPLidar('/dev/ttyUSB0')
	#range_min = lidar.get_min_range()
	#range_max = lidar.get_max_range()
	range_margin = 0.1
	
	
	#print(f"Range min: {range_min}, Range max: {range_max}")

	# try:
	# 	while True:
	
	scan_data = scan_processor.make_scan()
	#scan_data = [next(lidar.iter_measurments()) for _ in range(360)]
# set the maximum degree and the desired number of subsections
	max_index = len(scan_data)
	num_subsections = 4

	# calculate the size of each subsection dynamically
	subsection_size = int (max_index / num_subsections)



	# create an empty list to hold the results
	walls = []

	# call the function for each subsection and add the result to the list
	for i in range(num_subsections):
		start_index = int ((i+1) * subsection_size - subsection_size/18)
		end_index = int ((i+1) * subsection_size + subsection_size/18)
		# start_index = int (i * subsection_size + subsection_size/2)
		# end_index = int ((i+1) * subsection_size + subsection_size/2)

		if end_index >= max_index:
			end_index = end_index - max_index
			# print(scan_data[end_index])
			subsection = scan_data[start_index:max_index] + scan_data[0:end_index]
		else:
			subsection = scan_data[start_index:end_index]
		walls.append(subsection) 
		#with open("rplidar_data.txt","a") as f:
		#	for item in walls:
		#		for w in item:
		#			f.write(f"{w},") 
	#wal = walls[0]+walls[1]+walls[2]+walls[3]
	#plotpol(wal)
	#print(walls)

	# except KeyboardInterrupt:
	# 	print('Stopping...')

	# lidar.stop()
	# lidar.disconnect()

	return walls, scan_data

#output_lidar()
