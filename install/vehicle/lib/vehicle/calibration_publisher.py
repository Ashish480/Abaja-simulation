# calibration_publisher.py
import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool

class CalibrationPublisher(Node):
    def __init__(self):
        super().__init__('calibration_publisher')
        self.publisher_ = self.create_publisher(Bool, '/calibrated', 10)
        
        # Publish a single message with `data=True`
        msg = Bool()
        msg.data = True
        self.publisher_.publish(msg)
        self.get_logger().info("Published 'true' to /calibrated topic")

def main(args=None):
    rclpy.init(args=args)
    node = CalibrationPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

