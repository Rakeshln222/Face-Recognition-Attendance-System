# recognize_lbph.py
import cv2, pickle, sqlite3
from datetime import datetime
import numpy as np

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("recognizer.yml")

with open("labels.pickle","rb") as f:
    label_ids = pickle.load(f)
# invert dict
labels = {v:k for k,v in label_ids.items()}

conn = sqlite3.connect("attendance.db")
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, date TEXT, time TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)""")
conn.commit()

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rects = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    for (x,y,w,h) in rects:
        roi = cv2.resize(gray[y:y+h, x:x+w], (200,200))
        label_id, confidence = recognizer.predict(roi)  # lower confidence = better match
        if confidence < 80:  # threshold (tune >60)
            name = labels.get(label_id, "Unknown")
            cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
            cv2.putText(frame, f"{name} {int(confidence)}",(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,255,0),2)

            date_str = datetime.now().strftime("%Y-%m-%d")
            time_str = datetime.now().strftime("%H:%M:%S")
            cur.execute("SELECT COUNT(*) FROM attendance WHERE name=? AND date=?", (name, date_str))
            if cur.fetchone()[0] == 0:
                cur.execute("INSERT INTO attendance (name, date, time) VALUES (?, ?, ?)", (name, date_str, time_str))
                conn.commit()
                print(f"Marked {name} at {time_str}")

    cv2.imshow("LBPH Attendance", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
conn.close()
