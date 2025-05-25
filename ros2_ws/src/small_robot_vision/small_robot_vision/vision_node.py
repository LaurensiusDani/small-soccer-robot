import rclpy
from rclpy.node import Node
import cv2
import numpy as np
from geometry_msgs.msg import Point  # Tambahan untuk publish posisi

class VisionNode(Node):
    def __init__(self):
        super().__init__('vision_node')
        self.get_logger().info('VisionNode started')
        self.cap = cv2.VideoCapture(0) # Ganti angkanya kalo kameranya salah
        if not self.cap.isOpened():
            self.get_logger().error('Kamera tidak dapat dibuka')
            exit(1)
        self.publisher_ = self.create_publisher(Point, '/ball_position', 10)
        self.timer = self.create_timer(0.05, self.timer_callback)
    def timer_callback(self):
        ret, frame = self.cap.read()
        if not ret:
            self.get_logger().warn('Gagal membaca frame dari kamera')
            return
        self.detect_ball(frame)
    def detect_ball(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_yellow = np.array([20, 100, 100]) #TODO: Asumsiku bolanya kuning, nanti sesuain sama riilny
        
        upper_yellow = np.array([30, 255, 255])
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            largest = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(largest)
            if radius > 10:
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                cv2.putText(frame, "Bola Kuning", (int(x)-20, int(y)-20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255), 2)
                self.get_logger().info(f"Bola terdeteksi di ({int(x)}, {int(y)}), radius: {int(radius)})")
                point = Point()
                point.x = float(x)
                point.y = float(y)
                point.z = 0.0
                self.publisher_.publish(point)
        cv2.imshow("Deteksi Bola Kuning", frame)
        cv2.waitKey(1)

    def destroy_node(self):
        self.cap.release()
        cv2.destroyAllWindows()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = VisionNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
