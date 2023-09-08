import cv2
face_cap = cv2.CascadeClassifier('haarcastle.xml')
video_cap = cv2.VideoCapture(0)
while True:
    ret, video_data = video_cap.read()
    col=cv2.cvtColor(video_data, cv2.COLOR_BGR2GRAY)
    #we are making faces variable now
    faces= face_cap.detectMultiScale(
        col,
        scaleFactor= 1.1,
        minNeighbors=5,
        minSize=(30,30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    #now for rectangle mark
    for(x,y,w,h) in faces:
        cv2.rectangle(video_data, (x,y),(x+w, y+h),(255,0,0),3) #3 is width

    cv2.imshow('Camera Feed', video_data)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
video_cap.release()
cv2.destroyAllWindows()
