# FinalProject-Zumo
Final project for EE B.Sc. - Building a LiDAR controlled rover.

This project aims to develop an autonomous car capable of navigating inside an arena while maintaining a constant distance from its walls. By utilizing technologies such as ROS2, RPLiDAR, Raspberry Pi, ZumoPi model, RANSAC, and PID algorithms, the project explores the development of robust autonomous systems, control systems, and perception sensors. The main deliverable of this project is a fully functional autonomous car that demonstrates the effectiveness of ROS2 and Ubuntu 22 as a platform for such projects. The project incorporates a combination of hardware and software components, with the Raspberry Pi serving as the main processing unit. The RANSAC algorithm processes the LiDAR data to identify wall equations, while the PID algorithm calculates the appropriate steering angle and speed to maintain the desired distance from the walls. The system achieves high accuracy in maintaining the distance and angle from the walls. 


![image](https://github.com/liavr6/FinalProject-Zumo/assets/56167356/1184ef9d-3194-4e98-9c5f-3c28954a8271)


Figure 1 shows the physical layout of the autonomous car, with the LiDAR at the top of it.

![image](https://github.com/liavr6/FinalProject-Zumo/assets/56167356/588d3504-d8cb-4489-bad2-acb2bd8793ff)

Figure 2 shows the different modules (both physical and logical) of the system

![image](https://github.com/liavr6/FinalProject-Zumo/assets/56167356/666aecde-4f2c-4eae-8ec7-d966a35484c9)

Figure 3 shows the distance from the wall to the robot's right as a function of the time in a 15+ minutes run.
