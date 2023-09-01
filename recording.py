import cv2
import datetime
import os

def record(frame):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    cv2.putText(frame, current_time, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    return frame

cap = cv2.VideoCapture(0)

fourcc = cv2.VideoWriter_fourcc(*'XVID')  
output_folder = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
os.makedirs(output_folder, exist_ok=True)
output_file = os.path.join(output_folder, f'{output_folder}.avi')
fps = 30.0  
out = cv2.VideoWriter(output_file, fourcc, fps, (1300, 620))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    processed_frame = record(frame)
    
    cv2.imshow('Surveillance', processed_frame)

    out.write(processed_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()

cv2.destroyAllWindows()

