from ultralytics import YOLO
from threading import Thread
import cvzone
import cv2
import math
from Smail import send_email

model = YOLO("fireModel.pt")
classnames = ["fire"]

def fire(frame):
    result = model(frame,stream=True)
    EMstatus = False
    thread1 = Thread(target=send_email)
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
            if confidence>30 and EMstatus == False:
                thread1.start()
                EMstatus = True

    return frame
