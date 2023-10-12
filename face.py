import face_recognition
import cv2
import os
import math

def face():
    def load_known_faces(known_faces_folder):
        known_face_encodings = []
        known_face_names = []

        for file in os.listdir(known_faces_folder):
            image = face_recognition.load_image_file(os.path.join(known_faces_folder, file))
            face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=2)  
            if len(face_locations) == 0:
                print(f"No face found in {file}. Skipping...")
                continue

            face_encoding = face_recognition.face_encodings(image, face_locations)[0]
            known_face_encodings.append(face_encoding)
            known_face_names.append(file.split('.')[0])

        return known_face_encodings, known_face_names

    def face_confidence(face_distance):
        range=(1.0-0.6)
        linear_val=(1.0-face_distance)/(range*2.0)
        if face_distance > 0.6:
            return str(round(linear_val*100, 2))+'%'
        else:
            value=(linear_val+((1.0-linear_val)*math.pow((linear_val-0.5)*2, 0.2)))*100
            return str(round(value, 2))+'%'

    known_faces_folder = "known_faces"
    video_capture = cv2.VideoCapture(0)  

    known_face_encodings, known_face_names = load_known_faces(known_faces_folder)
    cv2.namedWindow("Video", cv2.WINDOW_GUI_NORMAL)

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        face_locations = face_recognition.face_locations(frame, number_of_times_to_upsample=2)  
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.6)  

            if any(matches):
                match_index = matches.index(True)
                name = known_face_names[match_index]
                confidence = face_confidence(face_recognition.face_distance([known_face_encodings[match_index]], face_encoding)[0])
            else:
                name = "Unknown"
                confidence = "N/A"

            top, right, bottom, left = face_locations[0]
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.putText(frame, f'{name} ({confidence})', (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 1)

        cv2.imshow("Video", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    face()
