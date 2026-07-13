import cv2
from ultralytics import YOLO
import sys

print("Loading model...")
model = YOLO('models/yolov8n.pt')
print("Opening video stream...")
cap = cv2.VideoCapture('udpsrc port=5600 ! application/x-rtp, payload=96 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! appsink', cv2.CAP_GSTREAMER)

success = False
for _ in range(30):
    ret, frame = cap.read()
    if ret:
        success = True
        break
    cv2.waitKey(100)

if success:
    print("Frame grabbed! Running YOLO...")
    results = model(frame, conf=0.01)
    for r in results:
        for box in r.boxes:
            print(f"Detected: {model.names[int(box.cls[0])]} | Conf: {float(box.conf[0]):.4f}")
    cv2.imwrite('capture_test.jpg', frame)
    print("Saved capture_test.jpg")
else:
    print("Failed to grab frame from stream.")
cap.release()
