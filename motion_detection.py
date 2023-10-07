import threading
import winsound
import imutils
import cv2

vid=cv2.VideoCapture(0,cv2.CAP_DSHOW)


vid.set(cv2.CAP_PROP_FRAME_WIDTH,640)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT,480)

ref,start_frame=vid.read()
start_frame=imutils.resize(start_frame,width=500)
start_frame=cv2.cvtColor(start_frame,cv2.COLOR_BGR2GRAY)
start_frame=cv2.GaussianBlur(start_frame,(21,21),0)

alarm=False
alarm_mode=False
alarm_count=0

def deep_alarm():
    global alarm
    for _ in range(5):
        if not alarm_mode:
            break
        print("ALARM")
        winsound.Beep(2500,1000)
    alarm=False


while True:
    ref,frame=vid.read()
    frame=imutils.resize(frame,width=500)

    if alarm_mode:
        frame_bw=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        frame_bw=cv2.GaussianBlur(frame_bw,(5,5),0)

        difference=cv2.absdiff(frame_bw,start_frame)
        threshold=cv2.threshold(difference,25,255,cv2.THRESH_BINARY)[1]
        start_frame=frame_bw

        if threshold.sum()>100000:
            alarm_count+=1
        else:
            if alarm_count>0:
                alarm_count-=1

        cv2.imshow("vid",threshold)
    else:
        cv2.imshow("vid",frame)

    if alarm_count>20:
        if not alarm:
            alarm=True
            threading.Thread(target=deep_alarm).start()

    key_press=cv2.waitKey(30)
    if key_press==ord('t'):
        alarm_mode=not alarm_mode
        alarm_count=0

    if key_press==ord('q'):
        alarm_mode=False
        break

vid.release()
cv2.destroyAllWindows()

