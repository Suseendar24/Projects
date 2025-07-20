from flask import Flask, Response
import cv2
app = Flask(__name__)
camera = cv2.VideoCapture(0)
def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Encode the frame as JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            # Yield frame to browser
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
@app.route('/')
def index():
    return "Camera is running. Go to /video_feed to see the video."
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/capture')
def capture():
    ret, frame = camera.read()
    if ret:
        cv2.imwrite("capture.jpg", frame)
        return "Image Captured and Saved as capture.jpg"
    else:
        return "Failed to capture image"
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
