from ultralytics import YOLO
import datetime
import cvzone
import cv2
import threading
import math
import os
from Smail import send_email
import flags

model = YOLO("assets/models/faceModel.pt")
classnames = ["face"]
    
def face(frame):
    output_folder = "Captured"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    result = model(frame, stream=True)

    for info in result:
        boxes = info.boxes
        for box in boxes:
            confidence = box.conf[0]
            confidence = math.ceil(confidence * 100)
            Class = int(box.cls[0])
            if confidence > 30:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
                cvzone.putTextRect(frame, f"{classnames[Class]}", [x1-8, y1-10], scale=1.5, thickness=2)
            if confidence > 80 and not flags.prohibited_email:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                output_path = os.path.join(output_folder, f"face_{timestamp}.jpg")
                cv2.imwrite(output_path, frame)
                flags.prohibited_email = True
                message = "Someone was detected in prohibited area"
                threading.Thread(target=send_email,args=[message,output_path]).start() 
    return frame


def faceCounter(frame):
    output_folder = "Captured"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    result = model(frame, stream=True)
    faceDetected = 0

    current_hour = datetime.datetime.now().hour
    restricted_time = False
    if 17<current_hour or current_hour<8:
        restricted_time = True

    for info in result:
        boxes = info.boxes
        for box in boxes:
            confidence = box.conf[0]
            confidence = math.ceil(confidence * 100)
            # if confidence > 40:
            #     faceDetected += 1
            #     text = f"No. of Peoples: {faceDetected}"
            #     position = (frame.shape[1] - 300, 50)
            #     cv2.putText(frame, text, position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            if faceDetected > 1 and not flags.restricted_email and restricted_time:
                current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                output_path = os.path.join(output_folder, f"face_{current_time}.jpg")
                cv2.imwrite(output_path, frame)
                flags.restricted_email = True
                message = f"Security Breach!!  {faceDetected} people were detected in restricted area"
                threading.Thread(target=send_email,args=[message,output_path]).start()        
    return frame
