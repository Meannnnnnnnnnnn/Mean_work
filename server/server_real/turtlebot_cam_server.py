# from flask import Flask, request
# import cv2
# import numpy as np

# app = Flask(__name__)

# @app.route('/upload', methods=['POST'])
# def upload_image():
#     if 'image' not in request.files:
#         return "No image found in request", 400

#     image_file = request.files['image']
#     npimg = np.frombuffer(image_file.read(), np.uint8)
#     img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
#     # Here you can process the image as needed
#     cv2.imwrite('received_image.jpg', img)
#     return "Image received", 200

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, Response, render_template
import cv2

app = Flask(__name__, template_folder='template')

def gen_frames():
    while True:
        frame = cv2.imread('/tmp/latest_frame.jpg')
        if frame is not None:
            _, jpeg = cv2.imencode('.jpg', frame)
            frame = jpeg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/')
def index():
    return render_template('cam_server.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
