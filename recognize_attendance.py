# recognize_attendance.py
import cv2, pickle, face_recognition, sqlite3, os
import numpy as np
from datetime import datetime

# load encodings
with open("encodings.pickle","rb") as f:
    data = pickle.load(f)

# SQLite DB
db_path = "attendance.db"
conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    date TEXT,
    time TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

cap = cv2.VideoCapture(0)
print("Press 'q' to quit and export CSV.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    small = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
    rgb_small = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)

    boxes = face_recognition.face_locations(rgb_small, model="hog")
    encodings_frame = face_recognition.face_encodings(rgb_small, boxes)

    for encoding, box in zip(encodings_frame, boxes):
        matches = face_recognition.compare_faces(data["encodings"], encoding, tolerance=0.5)
        distances = face_recognition.face_distance(data["encodings"], encoding)
        if len(distances) == 0:
            continue
        best_idx = np.argmin(distances)
        if matches[best_idx]:
            name = data["names"][best_idx]
            top, right, bottom, left = box
            # scale back up
            top, right, bottom, left = top*2, right*2, bottom*2, left*2
            cv2.rectangle(frame, (left, top), (right, bottom), (0,255,0), 2)
            cv2.putText(frame, name, (left, top-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)

            # Attendance logic: once per date
            date_str = datetime.now().strftime("%Y-%m-%d")
            time_str = datetime.now().strftime("%H:%M:%S")
            cur.execute("SELECT COUNT(*) FROM attendance WHERE name=? AND date=?", (name, date_str))
            already = cur.fetchone()[0]
            if already == 0:
                cur.execute("INSERT INTO attendance (name, date, time) VALUES (?, ?, ?)", (name, date_str, time_str))
                conn.commit()
                print(f"Marked attendance for {name} at {time_str} on {date_str}")

    cv2.imshow("Attendance", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Export to CSV
import pandas as pd
df = pd.read_sql_query("SELECT * FROM attendance ORDER BY timestamp DESC", conn)
csv_path = "attendance_export.csv"
df.to_csv(csv_path, index=False)
print("Exported:", csv_path)

conn.close()
