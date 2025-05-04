import os
import cv2
import numpy as np
import pickle
import face_recognition
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC

# Define dataset path
dataset_path = "dataset/students"

# Function to load images and extract face encodings
def load_faces_and_labels(folder_path):
    encodings = []
    labels = []

    if not os.path.exists(folder_path):
        print(f"⚠ Warning: {folder_path} does not exist!")
        return encodings, labels

    for person_name in os.listdir(folder_path):
        person_path = os.path.join(folder_path, person_name)

        if os.path.isdir(person_path):
            for image_name in os.listdir(person_path):
                image_path = os.path.join(person_path, image_name)

                # Load image
                image = cv2.imread(image_path)
                if image is None:
                    print(f"⚠ Warning: Cannot read {image_path}")
                    continue

                # Convert to RGB (face_recognition requires RGB)
                rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                # Detect face and get encodings
                face_locations = face_recognition.face_locations(rgb_image)
                face_encodings = face_recognition.face_encodings(rgb_image, face_locations)

                if face_encodings:
                    encodings.append(face_encodings[0])  # Store the first face encoding
                    labels.append(person_name)  # Use folder name as label
                else:
                    print(f"⚠ No face detected in {image_path}")

    return encodings, labels

# Load student images and extract features
print("🔍 Training Face Recognition Model...")
face_encodings, face_labels = load_faces_and_labels(dataset_path)

if not face_encodings:
    print("❌ Error: No valid faces found for training!")
    exit()

# Convert labels to numerical values
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(face_labels)

# Train SVM model
model = SVC(kernel="linear", probability=True)
model.fit(face_encodings, y_encoded)

# Save trained model and label encoder
with open("models/face_recognition_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("models/label_encoder.pkl", "wb") as f:
    pickle.dump(label_encoder, f)

print("✅ Model training complete! Faces are now properly recognized.")
