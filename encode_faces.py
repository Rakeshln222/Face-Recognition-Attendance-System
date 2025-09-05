# encode_faces.py
import os, cv2, pickle, face_recognition, numpy as np

dataset_dir = "dataset"
encodings = []
names = []

for person in os.listdir(dataset_dir):
    person_dir = os.path.join(dataset_dir, person)
    if not os.path.isdir(person_dir):
        continue
    for img_name in os.listdir(person_dir):
        img_path = os.path.join(person_dir, img_name)
        img = cv2.imread(img_path)
        if img is None: 
            continue
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb, model="hog")  # 'hog' faster on CPU
        face_encs = face_recognition.face_encodings(rgb, boxes)
        if len(face_encs) > 0:
            encodings.append(face_encs[0])
            names.append(person)

data = {"encodings": encodings, "names": names}
with open("encodings.pickle","wb") as f:
    pickle.dump(data, f)
print("Saved encodings.pickle with", len(encodings), "faces")
