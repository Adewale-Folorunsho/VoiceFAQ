# from flask import Flask,render_template,Response
# import cv2
# import os
# import sys

# filename = 'video.avi'
# frames_per_second = 24.0
# res = '720p'

# # Set resolution for the video capture
# # Function adapted from https://kirr.co/0l6qmh
# def change_res(cap, width, height):
#     cap.set(3, width)
#     cap.set(4, height)

# # Standard Video Dimensions Sizes
# STD_DIMENSIONS =  {
#     "480p": (640, 480),
#     "720p": (1280, 720),
#     "1080p": (1920, 1080),
#     "4k": (3840, 2160),
# }


# # grab resolution dimensions and set video capture to it.
# def get_dims(cap, res='1080p'):
#     width, height = STD_DIMENSIONS["480p"]
#     if res in STD_DIMENSIONS:
#         width,height = STD_DIMENSIONS[res]
#     ## change the current caputre device
#     ## to the resulting resolution
#     change_res(cap, width, height)
#     return width, height

# # Video Encoding, might require additional installs
# # Types of Codes: http://www.fourcc.org/codecs.php
# VIDEO_TYPE = {
#     'avi': cv2.VideoWriter_fourcc(*'XVID'),
#     #'mp4': cv2.VideoWriter_fourcc(*'H264'),
#     'mp4': cv2.VideoWriter_fourcc(*'XVID'),
# }

# def get_video_type(filename):
#     filename, ext = os.path.splitext(filename)
#     if ext in VIDEO_TYPE:
#       return  VIDEO_TYPE[ext]
#     return VIDEO_TYPE['avi']

# app=Flask(__name__)
# camera=cv2.VideoCapture(0)
# out = cv2.VideoWriter(filename, get_video_type(filename), 24, get_dims(camera, res))

# def generate_frames():
#     while True:
#         ## read the camera frame
#         success,frame=camera.read()
#         out.write(frame)
#         if not success:
#             break
#         else:
#             ret,buffer=cv2.imencode('.jpg',frame)
#             frame=buffer.tobytes()

#         yield(b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/video')
# def video():
#     return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

# if __name__=="__main__":
#     app.run(debug=True)

import numpy as np
import os
import cv2


filename = 'video.avi'
frames_per_second = 24.0
res = '720p'

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

# Video Encoding, might require additional installs
# Types of Codes: http://www.fourcc.org/codecs.php
VIDEO_TYPE = {
    'avi': cv2.VideoWriter_fourcc(*'XVID'),
    #'mp4': cv2.VideoWriter_fourcc(*'H264'),
    'mp4': cv2.VideoWriter_fourcc(*'XVID'),
}

def get_video_type(filename):
    filename, ext = os.path.splitext(filename)
    if ext in VIDEO_TYPE:
      return  VIDEO_TYPE[ext]
    return VIDEO_TYPE['avi']



cap = cv2.VideoCapture(0)
out = cv2.VideoWriter(filename, get_video_type(filename), 25, get_dims(cap, res))

while True:
    ret, frame = cap.read()
    out.write(frame)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
out.release()
cv2.destroyAllWindows()