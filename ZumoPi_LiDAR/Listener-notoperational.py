import math
import time

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import os

class LidarScanner(Node):
    def __init__(self):
        super().__init__("lidar_scanner")

        self.create_subscription(LaserScan, "scan", self.scan_callback, 10)

        self.optimal_distance = 0.1
        self.margin = 0.1
	
    def scan(self, msg):
        #self.get_logger().info(msg)
        return msg

    def scan_callback(self, msg):
        os.system('clear')
        range_at_45_degrees = msg.ranges[len(msg.ranges) // 4]
        range_at_90_degrees = msg.ranges[len(msg.ranges) // 2]
        range_at_135_degrees = msg.ranges[(len(msg.ranges) // 4) * 3]

        if abs(range_at_90_degrees - self.optimal_distance) <= self.margin:
            self.get_logger().info("Distance at 90 degrees is optimal")

        if abs(range_at_45_degrees - range_at_90_degrees) <= self.margin and abs(
            range_at_135_degrees - range_at_90_degrees
        ) <= self.margin:
            self.get_logger().info(f"Distances at 45, 90, and 135 degrees are the same within a margin of {self.margin}")
        else:
            self.get_logger().info("Distances at 45, 90, and 135 degrees are not the same")

        #wall_angle = math.degrees(math.atan2(range_at_45_degrees - range_at_135_degrees, 0.2))
        wall_angle = 90 - math.degrees(math.atan2(range_at_45_degrees - range_at_135_degrees, range_at_90_degrees)) 
        lidar_placement_angle = -45

        angle_45_degrees = lidar_placement_angle + wall_angle - 45
        angle_90_degrees = lidar_placement_angle + wall_angle
        angle_135_degrees = lidar_placement_angle + wall_angle + 45
        angle_wall = wall_angle# - 90

        self.get_logger().info(f"Angles: 45={angle_45_degrees:.2f}°, 90={angle_90_degrees:.2f}°, 135={angle_135_degrees:.2f}°, wall={angle_wall:.2f}°")
        

    def main(self):
        rclpy.spin(self)
        os.system('clear')


if __name__ == "__main__":
    rclpy.init()
    node = LidarScanner()
    node.main()
    rclpy.shutdown() 