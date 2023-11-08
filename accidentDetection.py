from threading import Thread
from ultralytics import YOLO
import cvzone
import cv2
import datetime
import math
import os
from Smail import send_email
import flags 
model = YOLO("assets/models/carModel.pt")
classnames = ["accident"]

def accident(frame):
    output_folder = "Captured"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

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
                cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),5)
                cvzone.putTextRect(frame, f"{classnames[Class]}", [x1-8,y1-10], scale=1.5, thickness=2)
            if confidence > 80 and not flags.accident_email:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                output_path = os.path.join(output_folder, f"crash_{timestamp}.jpg")
                cv2.imwrite(output_path, frame)
                flags.accident_email = True
                message = "Car Accident Alert"
                send_email(message,output_path)
              
                
    return frame