# capture_dataset.py
import cv2, os

name = input("Enter person name (no spaces): ").strip()
folder = os.path.join("dataset", name)
os.makedirs(folder, exist_ok=True)

cap = cv2.VideoCapture(0)
print("Press SPACE to capture an image. Press 'q' to quit.")
count = len(os.listdir(folder))

while True:
    ret, frame = cap.read()
    if not ret:
        print("Camera error")
        break
    cv2.putText(frame, f"Images captured: {count}", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
    cv2.imshow("Capture", frame)
    k = cv2.waitKey(1) & 0xFF
    if k == 32:  # SPACE
        count += 1
        path = os.path.join(folder, f"{count}.jpg")
        cv2.imwrite(path, frame)
        print("Saved", path)
    elif k == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
