from ultralytics import YOLO
import cvzone
import cv2
import math


# cap = cv2.VideoCapture(0)
model = YOLO("faceModel.pt")

classnames = ["face"]
def face(frame):
# while True:
    # ret, frame = cap.read()
    # frame = cv2.resize(frame,(640,480))
    result = model(frame,stream=True)
    EMstatus = False
    
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
                cvzone.putTextRect(frame, f'{classnames[Class]} {confidence}%', [x1+8,y1+100], scale=1.5, thickness=2)
    return frame
    # cv2.imshow("frame", frame)
    # if cv2.waitKey(20) & 0xFF==ord("p"):
            # break

# frame.release()
# cv2.destroyAllWindows