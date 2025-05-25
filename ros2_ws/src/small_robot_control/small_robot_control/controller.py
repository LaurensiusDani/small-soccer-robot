import rclpy
import time
from rclpy.node import Node
from geometry_msgs.msg import Twist

class RobotController(Node):
    def _init_(self):
        super()._init_('robot_controller')
        self.get_logger().info('RobotController node started')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
    def move(self, linear, angular):
        msg = Twist()
        msg.linear.x = linear     # Maju/mundur
        msg.angular.z = angular   # Kiri/kanan
        self.publisher_.publish(msg)
        self.get_logger().info(f"Gerak: linear={linear}, angular={angular}")
def main(args=None):
    rclpy.init(args=args)
    node = RobotController()
    try:
        start_time = time.time()
        while time.time() - start_time < 5:
            node.move(0.2, 0.0)  
            time.sleep(0.1)
        node.move(0.0, 0.0)  
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()

if _name_ == '_main_':
    main()
