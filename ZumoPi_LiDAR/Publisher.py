import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from sensor_msgs.msg import LaserScan
from rplidar import RPLidar
import argparse
import math

class RPLidarNode(Node):
    def __init__(self):
        super().__init__('rplidar_node')

        # Get parameters from the command line or set defaults
        parser = argparse.ArgumentParser()
        parser.add_argument('-p', '--serial_port', type=str, default='/dev/ttyUSB0')
        parser.add_argument('-f', '--frame_id', type=str, default='lidar_link')
        parser.add_argument('-c', '--angle_compensate', type=bool, default=True)
        parser.add_argument('-m', '--scan_mode', type=str, default='BOOST')
        args = parser.parse_args()

        # Set up the RPLidar sensor
        self.lidar = RPLidar(args.serial_port)
        self.lidar.stop_motor()
        self.lidar.start_motor()
        self.scan_mode = getattr(RPLidar, 'MODE_' + args.scan_mode.upper())
        self.lidar.set_scan_mode(self.scan_mode)

        # Set up the ROS publisher
        qos_profile = QoSProfile(depth=10)
        self.publisher_ = self.create_publisher(LaserScan, 'scan', qos_profile)

        # Set up the ROS timer to publish scans
        self.timer = self.create_timer(0.1, self.publish_scan_data)

        # Set up the ROS message for scans
        self.msg = LaserScan()
        self.msg.header.frame_id = args.frame_id
        self.msg.angle_increment = math.radians(360.0 / 360)
        self.msg.range_min = 0.15
        self.msg.range_max = 8.0

    def publish_scan_data(self):
        try:
            scan_data = self.lidar.iter_scans()
            data = next(scan_data)
            ranges = [item[1] for item in data]
            self.msg.header.stamp = self.get_clock().now().to_msg()
            self.msg.ranges = ranges
            self.publisher_.publish(self.msg)
        except StopIteration:
            pass

    def __del__(self):
        self.lidar.stop_motor()
        self.lidar.stop()


def main(args=None):
    rclpy.init(args=args)

    node = RPLidarNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main() 