import cv2
import face_recognition
import numpy as np
import os

# ✅ Load known faces and their encodings
def load_known_faces(dataset_path="dataset/students"):
    known_face_encodings = []
    known_face_names = []
    
    if not os.path.exists(dataset_path):
        print(f"⚠ Warning: Dataset folder {dataset_path} not found!")
        return known_face_encodings, known_face_names

    for person_name in os.listdir(dataset_path):
        person_path = os.path.join(dataset_path, person_name)

        # ✅ Skip non-directory files
        if not os.path.isdir(person_path):
            continue

        for image_name in os.listdir(person_path):
            image_path = os.path.join(person_path, image_name)

            if image_name.lower().endswith((".png", ".jpg", ".jpeg")):
                try:
                    image = face_recognition.load_image_file(image_path)
                    face_encodings = face_recognition.face_encodings(image)
                    
                    if face_encodings:
                        known_face_encodings.append(face_encodings[0])  # Store only first detected face encoding
                        known_face_names.append(person_name)  # Store corresponding student ID
                    
                except Exception as e:
                    print(f"⚠ Error processing {image_path}: {e}")

    return known_face_encodings, known_face_names

# ✅ Recognize faces from a camera frame (More Accurate)
# Recognize faces from camera frame
def recognize_faces(frame, known_encodings, known_names):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    recognized_ids = []
    
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_encodings, face_encoding)
        face_distances = face_recognition.face_distance(known_encodings, face_encoding)
        best_match_index = np.argmin(face_distances) if matches else None

        if best_match_index is not None and matches[best_match_index]:
            recognized_ids.append(known_names[best_match_index])  # ✅ Append student ID instead of index

    return recognized_ids
