# from flask import Flask, render_template, Response
# import cv2, time
# from threading import Thread, Lock

# # Create the Threaded Camera class because if directly use the cv2.VideoCapture(0), it call opens the default camera.
# # The camera is locked for use by the first process.
# # When a second device tries to access the video feed, the camera is already in use by the first process, so it cannot provide the feed.
# class Camera:
#     def __init__(self):
#         self.camera = cv2.VideoCapture(2)
#         (self.success, self.frame) = self.camera.read()
#         self.is_running = True
#         self.lock = Lock()
#         self.thread = Thread(target=self.update_frame, args=())
#         self.thread.start()

#     def update_frame(self):
#         while self.is_running:
#             (success, frame) = self.camera.read()
#             with self.lock:
#                 self.success = success
#                 self.frame = frame

#     def get_frame(self):
#         with self.lock:
#             if self.success:
#                 ret, buffer = cv2.imencode('.jpg', self.frame)
#                 return buffer.tobytes()
#             else:
#                 return None

#     def stop(self):
#         self.is_running = False
#         self.thread.join()
#         self.camera.release()

# # Initialize Flask app
# app = Flask(__name__, template_folder='template')

# # Create a global camera object
# camera = Camera()

# # Generator function to yield frames
# def gen_frames():
#     while True:
#         frame = camera.get_frame()
#         if frame is None:
#             continue
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# # Define the routes
# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/video_feed')
# def video_feed():
#     return Response(gen_frames(), mimetype='multipart/x-mixed-replace;boundary=frame')

# # Run the app
# if __name__ == '__main__':
#     try:
#         app.run(debug=True, host='0.0.0.0', port=8080)
#     finally:
#         camera.stop()


from flask import Flask, render_template, Response
import cv2
from threading import Thread, Lock
import time
from pathlib import Path

app = Flask(__name__, template_folder='template')

class VideoStreamWidget:
    def __init__(self, src=2):
        self.capture = cv2.VideoCapture(src)
        self.lock = Lock()
        self.status, self.frame = self.capture.read()
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        while True:
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read()
            time.sleep(0.01)
    
    def get_frame(self):
        with self.lock:
            if self.status:
                ret, buffer = cv2.imencode('.jpg', self.frame)
                return buffer.tobytes()
            else:
                return None

video_stream_widget = VideoStreamWidget()

def gen_frames():
    while True:
        frame = video_stream_widget.get_frame()
        if frame is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace;boundary=frame')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
