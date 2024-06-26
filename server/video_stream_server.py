import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from http.server import BaseHTTPRequestHandler, HTTPServer
import cv2
import threading

# Global variable to store the latest frame
latest_frame = None
bridge = CvBridge()

# ROS subscriber callback function
def image_callback(msg):
    global latest_frame
    latest_frame = bridge.imgmsg_to_cv2(msg, "bgr8")

# HTTP request handler class
class StreamHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=frame')
        self.end_headers()
        while True:
            if latest_frame is not None:
                ret, jpeg = cv2.imencode('.jpg', latest_frame)
                self.wfile.write(b'--frame\r\n')
                self.send_header('Content-Type', 'image/jpeg')
                self.send_header('Content-Length', len(jpeg.tobytes()))
                self.end_headers()
                self.wfile.write(jpeg.tobytes())
                self.wfile.write(b'\r\n')
            else:
                # If no frame is available, sleep briefly to avoid busy-waiting
                rospy.sleep(0.1)

# Function to start the HTTP server
def start_http_server():
    server_address = ('', 8080)  # Serve on all network interfaces on port 8080
    httpd = HTTPServer(server_address, StreamHandler)
    print("HTTP server running on port 8080")
    httpd.serve_forever()

if __name__ == '__main__':
    rospy.init_node('video_stream_server')
    rospy.Subscriber('video_stream', Image, image_callback)
    http_thread = threading.Thread(target=start_http_server)
    http_thread.start()
    rospy.spin()
