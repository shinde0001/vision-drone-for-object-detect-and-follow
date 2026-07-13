import cv2
import threading
import time
import numpy as np

class CameraStream:
    def __init__(self, port=5600):
        self.port = port
        self.frame = None
        self.running = False
        self.lock = threading.Lock()
        self.thread = None
        self.cap = None

    def start(self):
        self.running = True
        
        # Try GStreamer pipeline
        gst_str = f'udpsrc port={self.port} ! application/x-rtp,encoding-name=H264 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! appsink sync=false'
        self.cap = cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)
        
        if not self.cap.isOpened():
            # Fallback to JPEG
            gst_str2 = f'udpsrc port={self.port} ! application/x-rtp,payload=96 ! rtpjpegdepay ! jpegdec ! videoconvert ! appsink sync=false'
            self.cap = cv2.VideoCapture(gst_str2, cv2.CAP_GSTREAMER)
            
        if not self.cap.isOpened():
            # Fallback to raw UDP
            self.cap = cv2.VideoCapture(f'udp://127.0.0.1:{self.port}', cv2.CAP_FFMPEG)
            
        if not self.cap.isOpened():
            print(f"Error: Could not open video stream on port {self.port}")
            self.running = False
            return False
            
        print("Camera stream started successfully.")
        self.thread = threading.Thread(target=self._update, daemon=True)
        self.thread.start()
        return True

    def _update(self):
        while self.running:
            if self.cap is not None and self.cap.isOpened():
                ret, frame = self.cap.read()
                if ret:
                    with self.lock:
                        self.frame = frame
                else:
                    time.sleep(0.01)
            else:
                time.sleep(0.1)

    def get_frame(self):
        with self.lock:
            if self.frame is not None:
                return self.frame.copy()
            return None

    def stop(self):
        self.running = False
        if self.thread is not None:
            self.thread.join(timeout=1.0)
        if self.cap is not None:
            self.cap.release()
