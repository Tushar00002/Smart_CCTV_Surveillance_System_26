import cv2
import numpy as np
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import cv2

def capture_image(camera):

        return_value, image = camera.read()
        cv2.imwrite("captured_image.jpg", image)
        camera.release()
        cv2.destroyAllWindows()
        return "captured_image.jpg"




def send_email(message,image_filename):
        sender_email = "younliacmh@gmail.com"
        receiver_email = "ajmrhw12@gmail.com"
        subject="Smart CCTV"

        server = smtplib.SMTP('smtp.gmail.com', 587)  # SMPT server domain name and port 58704

        server.ehlo()
        server.starttls()
        server.login(sender_email, 'nkdnlfliltredjov')
        msg=MIMEMultipart()
        msg["subject"] = subject
        msg["From"]=sender_email
        msg["To"]=receiver_email

        msg.attach(MIMEText(message,"plain"))

        with open(image_filename,'rb') as attachment:
              image_data=attachment.read()
        image=MIMEImage(image_data,name=image_filename)
        msg.attach(image)

        server.sendmail(sender_email, receiver_email, msg.as_string())

        server.quit()
        print("Email sent successfully")



# Load Yolo
weg=r"C:\Users\younl\Downloads\yolov3_training_2000.weights"  
cfg= r"C:\Users\younl\Downloads\yolov3_testing.cfg"
net = cv2.dnn.readNet(weg,cfg )
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_DEFAULT)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
classes = ["Weapon"]

cap = cv2.VideoCapture(0)

while True:
    _, img = cap.read()
    height, width, channels = img.shape
    # width = 512
    # height = 512

    # Detecting objects
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)

    layer_names = net.getLayerNames()

    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    colors = np.random.uniform(0, 255, size=(len(classes), 3))
    outs = net.forward(output_layers)

    # Showing information on the screen
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    print(indexes)
    if indexes == 0:
        print("weapon detected in frame")
        file_name=capture_image(cap)
        message="weapon detected in frame"
        send_email(message,file_name)

    font = cv2.FONT_HERSHEY_PLAIN
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            color = colors[class_ids[i]]
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(img, label, (x, y + 30), font, 3, color, 3)

    # frame = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()