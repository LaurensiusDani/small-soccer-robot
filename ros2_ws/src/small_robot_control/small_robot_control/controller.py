import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import serial
import threading

class SerialCommNode(Node):
    def __init__(self):
        super().__init__('serial_comm_node')

        self.declare_parameter('port', '/dev/ttyUSB0')
        self.declare_parameter('baudrate', 115200)

        port = self.get_parameter('port').get_parameter_value().string_value
        baudrate = self.get_parameter('baudrate').get_parameter_value().integer_value

        try:
            self.ser = serial.Serial(port, baudrate, timeout=1.0)
            self.get_logger().info(f'Connected to serial port {port} at {baudrate} bps')
        except Exception as e:
            self.get_logger().error(f'Failed to open serial port: {e}')
            return

        self.publisher_ = self.create_publisher(String, 'from_serial', 10)
        self.subscription = self.create_subscription(String, 'to_serial', self.write_serial_callback, 10)

        self.thread = threading.Thread(target=self.read_serial)
        self.thread.daemon = True
        self.thread.start()

    def read_serial(self):
        while rclpy.ok():
            try:
                line = self.ser.readline().decode('utf-8').strip()
                if line:
                    msg = String()
                    msg.data = line
                    self.publisher_.publish(msg)
            except Exception as e:
                self.get_logger().error(f'Error reading from serial: {e}')

    def write_serial_callback(self, msg):
        try:
            self.ser.write((msg.data + '\n').encode('utf-8'))
        except Exception as e:
            self.get_logger().error(f'Error writing to serial: {e}')

def main(args=None):
    rclpy.init(args=args)
    node = SerialCommNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
