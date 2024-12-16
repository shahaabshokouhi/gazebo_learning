#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class LidarStopNode(Node):
    def __init__(self):
        super().__init__('lidar_stop_node')

        # Publisher for /cmd_vel
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)

        # Subscriber for /lidar
        self.subscription = self.create_subscription(
            LaserScan,
            '/lidar',
            self.lidar_callback,
            10
        )

        self.get_logger().info("LidarStopNode is up and running.")

    def lidar_callback(self, msg):
        # Process LaserScan message
        all_more = all(r > 1.0 for r in msg.ranges if r > 0.0)  # Ignore invalid ranges (<= 0)

        twist_msg = Twist()
        if all_more:
            # Move forward
            twist_msg.linear.x = 0.5
            twist_msg.angular.z = 0.0
        else:
            # Rotate in place
            twist_msg.linear.x = 0.0
            twist_msg.angular.z = 0.5

        # Publish Twist message
        self.publisher.publish(twist_msg)
        self.get_logger().info(f"Published: {twist_msg}")

def main(args=None):
    rclpy.init(args=args)

    # Create and spin the node
    node = LidarStopNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
