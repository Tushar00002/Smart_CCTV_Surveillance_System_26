import os
import cv2
from PIL import Image
import numpy as np

face_classifier = cv2.CascadeClassifier('assets/models/haarcascade_frontalface_default.xml')

def face_extractor(img):
    output_folder = "assets/storedFaces"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray,1.3,5)

    if faces is():
        return None

    for(x,y,w,h) in faces:
        cropped_face = img[y:y+h, x:x+w]

    return cropped_face

cap = cv2.VideoCapture(0)
id = int(input("Enter ID number: "))
img_id = 0

while True:
    ret, frame = cap.read()
    if face_extractor(frame) is not None:
        img_id+=1
        face = cv2.resize(face_extractor(frame),(200,200))
        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

        file_path = 'assets/storedFaces/user.'+str(id)+"."+str(img_id)+'.jpg'

        cv2.imwrite(file_path,face)

        cv2.putText(face,str(img_id),(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
        cv2.imshow('Face Cropper',face)
    else:
        print("Face not found")
        pass

    if cv2.waitKey(1)==13 or img_id==100:
        break

cap.release()
cv2.destroyAllWindows()
print('Samples Colletion Completed ')
