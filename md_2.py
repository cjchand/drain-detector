# import the necessary packages
from pyimagesearch.tempimage import TempImage
import argparse
import warnings
import datetime
import imutils
import json
import time
import cv2
from moviepy.editor import *
 
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--conf", required=True, help="path to the JSON configuration file")
ap.add_argument("-v", "--video", help="path to the video file")
args = vars(ap.parse_args())
 
# filter warnings, load the configuration and initialize the Dropbox
# client
warnings.filterwarnings("ignore")
conf = json.load(open(args["conf"]))
client = None
avg = None
drain_times = []

# if the video argument is None, then we are reading from webcam
if args.get("video", None) is None:
    vs = VideoStream(src=0).start()
    time.sleep(2.0)

# otherwise, we are reading from a video file
else:
    vs = cv2.VideoCapture(args["video"])

# initialize the first frame in the video stream
firstFrame = None

# loop over the frames of the video
while True:
    # grab the current frame and initialize the occupied/unoccupied
    # text
    frame = vs.read()
    frame = frame if args.get("video", None) is None else frame[1]
    text = "Unoccupied"
    timestamp = datetime.datetime.now()

    # if the frame could not be grabbed, then we have reached the end
    # of the video
    if frame is None:
        break
    
    # print(type(frame))
    frame = imutils.resize(frame, width=500)
    frame = frame[770:815, 205:275]
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # if the average frame is None, initialize it
    if avg is None:
        print("[INFO] starting background model...")
        avg = gray.copy().astype("float")
        continue

    # accumulate the weighted average between the current frame and
    # previous frames, then compute the difference between the current
    # frame and running average
    cv2.accumulateWeighted(gray, avg, 0.5)
    frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))

    # threshold the delta image, dilate the thresholded image to fill
    # in holes, then find contours on thresholded image
    thresh = cv2.threshold(frameDelta, conf["delta_thresh"], 255,
        cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # loop over the contours
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < conf["min_area"]:
            continue

        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        new_drain_time = vs.get(cv2.CAP_PROP_POS_MSEC)
        if len(drain_times) == 0:
            drain_times.append(vs.get(cv2.CAP_PROP_POS_MSEC))
        if new_drain_time - drain_times[-1] > 10000:
            # I am hoping you don't drain 10 seconds after the prior drain :)
            drain_times.append(vs.get(cv2.CAP_PROP_POS_MSEC))
    
    # check to see if the frames should be displayed to screen
    if conf["show_video"]:
        # display the security feed
        cv2.imshow("Drain Monitor", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key is pressed, break from the lop
        if key == ord("q"):
            break

for i in range(1, len(drain_times), 1):
    # Times are in milliseconds
    drain_time = drain_times[i]/1000
    # Start the clip 10 seconds prior to the drain
    start_clip = drain_time - 10
    # End the clip 3 seconds after the drain
    end_clip = drain_time + 3
    print('Writing video file. Drain time: {}, Start clip: {}, End clip: {}'.format(drain_time, start_clip, end_clip))
    clip = VideoFileClip(args['video']).subclip(start_clip, end_clip)
    clip.write_videofile('drain_{}.mp4'.format(str(i)))