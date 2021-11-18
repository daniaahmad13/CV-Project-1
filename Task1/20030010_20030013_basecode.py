import urllib
import cv2
import numpy as np
import matplotlib.pyplot as plt
from threading import Thread

camera_url = {
    "Camera-1": "http://10.104.2.113:8080/video",
    "Camera-2": "http://10.104.1.66:8080/video",
    # "Camera-3": "http://10.104.1.90:8080/video",
    }


camera_number = {
    "Camera-1" : "1",
    "Camera-2" : "2",
    "Camera-3" : "3",
    }


def capture_video(name, url, video_path, dir_path, total_frames, frame_rate):
    # Record video
    windowName = "Sample Feed from" + name
    cv2.namedWindow(windowName)

    cam = cv2.VideoCapture(url)
    print(name, url)

    # define size for recorded video frame for video
    width1 = int(cam.get(3))
    height1 = int(cam.get(4))
    size1 = (width1, height1)

    # frame of size is being created and stored in .avi file
    video_name = dir_path + "/Videos/"+ "Stream" + camera_number.get(name) + "Recording" + ".avi"
    output_stream = cv2.VideoWriter(
        video_name, cv2.VideoWriter_fourcc(*'MJPG'), 10, size1)


    # check if feed exists or not for camera 1
    if cam.isOpened():
        ret, frame = cam.read()
    else:
        ret = False


    count_frames = 0
    
    while ret:
        print(count_frames)
        opened = cam.isOpened()
        
        if(opened == False):
            print(name,"Closed")
            return

        ret, frame = cam.read()        
        output_stream.write(frame)

        cv2.imshow(name, frame)

        count_frames += 1
        if cv2.waitKey(1) == 27:
            break
            
    cam.release()
    output_stream.release()
    print(name, "End.")
    cv2.destroyWindow(name)

def livefeed(name, url):
    windowName = "Live Stream from " + name
    cv2.namedWindow(windowName)

    cam = cv2.VideoCapture(url)
    print(name, url)

    if cam.isOpened():  # check if feed exists or not for camera
        ret, frame = cam.read()
    else:
        ret = False

    while ret:  # and ret2 and ret3:
        ret, frame = cam.read()
        cv2.imshow(windowName, frame)

        if cv2.waitKey(1) == 27:
            break

    cam.release()
    cv2.destroyAllWindows()


video_paths = []
output_streams = []
cams = []
names = []

seconds = 15
frame_rate = 10
total_frames = seconds * frame_rate
dir_path = r"C:\\Users\\Dell\\DataScience\\Lums\\CS5310\\MiniProject\\Task1"


def main():

    print("Press 1 for pre-recorded videos, 2 for live stream: ")
    option = int(input())

    if option == 1:
        # record videos
        for (name, url) in camera_url.items():
            video_path = dir_path + "/Videos/"+ name + ".avi"
            Thread(target=capture_video, args=(name, url, video_path, dir_path,total_frames, frame_rate)).start()

    elif option == 2:
        # live stream
        for (name, url) in camera_url.items():
            Thread(target=livefeed, args=(name, url)).start()

    else:
        print("Invalid option entered. Exiting...")

main()