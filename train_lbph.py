# train_lbph.py
import cv2, os, numpy as np, pickle
from pathlib import Path

dataset = "dataset"
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

faces = []
labels = []
label_ids = {}
current_id = 0

for person in os.listdir(dataset):
    person_dir = os.path.join(dataset, person)
    if not os.path.isdir(person_dir):
        continue
    if person not in label_ids:
        label_ids[person] = current_id
        current_id += 1
    id_ = label_ids[person]
    for img_name in os.listdir(person_dir):
        img_path = os.path.join(person_dir, img_name)
        img = cv2.imread(img_path)
        if img is None:
            continue
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        rects = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        for (x,y,w,h) in rects:
            roi = gray[y:y+h, x:x+w]
            faces.append(cv2.resize(roi, (200,200)))
            labels.append(id_)

faces_np = np.array(faces)
labels_np = np.array(labels)

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.train(faces_np, labels_np)
recognizer.write("recognizer.yml")

with open("labels.pickle","wb") as f:
    pickle.dump(label_ids, f)
print("Training complete. Labels:", label_ids)
