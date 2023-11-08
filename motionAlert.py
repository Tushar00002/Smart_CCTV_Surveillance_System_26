import threading
import winsound
import imutils
import cv2

alarm=False
alarm_mode=False
alarm_count=0

def beep_alarm():
    global alarm_count,alarm
    for _ in range(3):
        print("ALARM")
        winsound.Beep(2500,1000)
    alarm_count=0
    alarm=False

def motionDetector(frame):
    global alarm_count, alarm
    started = False
    if started == False:
        start_frame = frame
        started = True
    start_frame=imutils.resize(start_frame,width=500)
    start_frame=cv2.cvtColor(start_frame,cv2.COLOR_BGR2GRAY)
    frame=imutils.resize(frame,width=500)
    start_frame=cv2.GaussianBlur(start_frame,(21,21),0)
    frame_bw=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    frame_bw=cv2.GaussianBlur(frame_bw,(5,5),0)

    difference=cv2.absdiff(frame_bw,start_frame)
    threshold=cv2.threshold(difference,25,255,cv2.THRESH_BINARY)[1]
    start_frame=frame_bw

    if threshold.sum()>60000:
        alarm_count+=1
    else:
        if alarm_count>0:
            alarm_count-=1

    if alarm_count>20:
        if not alarm:
            alarm=True
            threading.Thread(target=beep_alarm).start()

# def main():
#     cam = cv2.VideoCapture(0)

#     while True:
#         ret, frame = cam.read()

#         cv2.imshow("video", frame)
#         motionDetector(frame)
        
#         if cv2.waitKey(20) & 0xFF==ord("p"):
#             break

# main()