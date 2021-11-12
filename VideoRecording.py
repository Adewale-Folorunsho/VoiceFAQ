from flask import Flask,render_template,Response
from fer import Video
from fer import FER
import cv2
import os
import sys
import pandas as pd
import signal

def teardown(x , y):
    camera.release()
    out.release()
    cv2.destroyAllWindows()

    # os.wait()
    #emotionDetector()
    sys.exit(0)

# def emotionDetector():
#     location_videofile = "/Users/adewalefolorunsho/Desktop/Voice_Faq_Project/faqVideoRecording.avi"

#     # Build the Face detection detector
#     face_detector = FER(mtcnn=True)
#     # Input the video for processing
#     input_video = Video(location_videofile) # process the video by frames

#     # The Analyze() fucnction will run analysis on every frame of the input video. 
#     # It will create a rectangular box around every image and show the emotion values next to that.
#     # Finally, the method will publish a new video that will have a box around the face of the human with live emotion values.
#     processing_data = input_video.analyze(face_detector, display=False) # analyze face using the FER detector

#     # We will now convert the analysed information into a dataframe.
#     # This will help us import the data as a .CSV file to perform analysis over it later
#     vid_df = input_video.to_pandas(processing_data)
#     vid_df = input_video.get_first_face(vid_df)
#     vid_df = input_video.get_emotions(vid_df)

#     # Plotting the emotions against time in the video
#     pltfig = vid_df.plot(figsize=(20, 8), fontsize=16).get_figure()

#     # We will now work on the dataframe to extract which emotion was prominent in the video
#     angry = sum(vid_df.angry)
#     disgust = sum(vid_df.disgust)
#     fear = sum(vid_df.fear)
#     happy = sum(vid_df.happy)
#     sad = sum(vid_df.sad)
#     surprise = sum(vid_df.surprise)
#     neutral = sum(vid_df.neutral)

#     emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
#     emotions_values = [angry, disgust, fear, happy, sad, surprise, neutral]

#     score_comparisons = pd.DataFrame(emotions, columns = ['Human Emotions'])
#     score_comparisons['Emotion Value from the Video'] = emotions_values
#     score_comparisons


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

def generate_frames():
    while True:
        success,frame=camera.read()
        out.write(frame)
        if not success:
            break
        else:
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

if __name__=="__main__":
    app.run(debug=True)


