from flask import Flask,render_template,Response
from fer import Video
from fer import FER
import cv2
import os
import sys
import pandas as pd
import signal

def teardown(x , y):
    print("got here")
    #print("got here")
    camera.release()
    out.release()
    sys.exit(0)


signal.signal(signal.SIGINT, teardown)
filename = 'faqVideoRecording.avi'
frames_per_second = 24.0
res = '720p'
#face_detector = FER(mtcnn=True)
app=Flask(__name__)
# Set resolution for the video capture
# Function adapted from https://kirr.co/0l6qmh
def change_res(cap, width, height):
    cap.set(3, width)
    cap.set(4, height)

# Standard Video Dimensions Sizes
STD_DIMENSIONS =  {
    "480p": (640, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "4k": (3840, 2160),
}

# grab resolution dimensions and set video capture to it.
def get_dims(cap, res='1080p'):
    width, height = STD_DIMENSIONS["480p"]
    if res in STD_DIMENSIONS:
        width,height = STD_DIMENSIONS[res]
    ## change the current caputre device
    ## to the resulting resolution
    change_res(cap, width, height)
    return width, height


camera=cv2.VideoCapture(0)
out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'XVID'), 25, get_dims(camera, res))
#vid_df = pd.DataFrame()

def generate_frames():
    while True:
        success,frame=camera.read()
        out.write(frame)
        if not success:
            break
        else:
            # input_video = Video("/video")
            # processing_data = input_video.analyze(face_detector, display=False)
            # vid_df.append(input_video.to_pandas(processing_data))
            ret,buffer=cv2.imencode('.jpg',frame)
            frame=buffer.tobytes()

        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

#@app.teardown_appcontext
def teardown(e):
    print(e)
    #print("got here")
    if e is not None:
        camera.release()
        out.release()

if __name__=="__main__":
    #try:
    app.run(debug=True)
    # except KeyboardInterrupt:
    #     print("got here")
    #     camera.release()
    #     out.release()
    #     try:
    #         sys.exit(0)
    #     except SystemExit:
    #         os._exit(0)


