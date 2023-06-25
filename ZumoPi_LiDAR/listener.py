import rclpy
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import LaserScan

"""def laser_callback(data):
    angle_inc = 0.008714509196579456 
    angle_min=-3.1241393089294434
    angle_max=3.1415927410125732    
    with open('rplidar_data.txt', 'a') as f:
        #print(data)
        #exit()
        ranges = data.ranges
        processed = []
        #print (data)
        for i in range(len(ranges)):
            #f.write("{}\n".format(ranges[i]))
            #print(f"{(angle_min+angle_inc*i)/angle_max*180}:{ranges[i]}") 
            processed.append([ranges[i],(angle_min+angle_inc*i)/angle_max*180])
            #print(processed)
        return processed

def make_scan():
    rclpy.init()
    node = rclpy.create_node('rplidar_listener')
    sub = node.create_subscription(LaserScan, '/scan', laser_callback, qos_profile=qos_profile_sensor_data)
    rclpy.spin(node)
    processed = laser_callback(last_message)  # get the result returned by laser_callback
    print(processed)  # do something with the result
    node.destroy_node()
    rclpy.shutdown()"""
class ScanProcessor:
    def __init__(self):
        self.processed_data = None

    def laser_callback(self, data):
        angle_inc = 0.008714509196579456 
        angle_min=-3.1241393089294434
        angle_max=3.1415927410125732    
        processed = []
        ranges = data.ranges
        for i in range(len(ranges)):
            processed.append([ranges[i],((angle_min+angle_inc*i)/angle_max)*180+180])
        self.processed_data = processed

    def make_scan(self):
        #rclpy.init()
        node = rclpy.create_node('rplidar_listener')
        sub = node.create_subscription(LaserScan, '/scan', self.laser_callback, qos_profile=qos_profile_sensor_data)
        try:
            while rclpy.ok():
                rclpy.spin_once(node, timeout_sec=0.1)
                if self.processed_data is not None:
                    # do something with the processed data
                    return(self.processed_data)
                    #self.processed_data = None
        except KeyboardInterrupt:
            pass
        
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    scan_processor = ScanProcessor()
    scan_processor.make_scan()

#make_scan()
