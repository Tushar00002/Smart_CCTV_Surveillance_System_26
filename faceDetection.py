from ultralytics import YOLO
from threading import Thread
import datetime
import cvzone
import cv2
import math
from Smail import send_email

model = YOLO("faceModel.pt")
classnames = ["face"]

def face(frame):

    result = model(frame,stream=True)
    
    for info in result:
        boxes = info.boxes
        for box in boxes:
            confidence = box.conf[0]
            confidence = math.ceil(confidence*100)
            Class = int(box.cls[0])
            if confidence>10:
                x1,y1,x2,y2 = box.xyxy[0]
                x1,y1,x2,y2 = int(x1),int(y1),int(x2),int(y2)
                cv2.rectangle(frame,(x1,y1),(x2,y2),(0,0,255),5)
                cvzone.putTextRect(frame, f'{classnames[Class]} {confidence}%', [x1-8,y1-10], scale=1.5, thickness=2)
    return frame

def faceCounter(frame):
    result = model(frame, stream=True)
    EMstatus = False
    thread2 = Thread(target=send_email)
    faceDetected = 0

    current_time = datetime.datetime.now()
    current_hour = current_time.hour
    restricted_time = False
    if 22<current_hour or current_hour<8:
        restricted_time == True

    for info in result:
        boxes = info.boxes
        for box in boxes:
            confidence = box.conf[0]
            confidence = math.ceil(confidence * 100)
            if confidence > 10:
                faceDetected += 1
            if faceDetected > 4 and EMstatus == False and restricted_time==True:
                thread2.start()
                EMstatus = True
