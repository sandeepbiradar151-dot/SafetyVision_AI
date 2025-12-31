import cv2
from ultralytics import YOLO
import torch
import asyncio
from backend.alert_manager import alert_manager

class VideoStreamer:
    def __init__(self):
        print("--- Loading AI Model ---")
        self.model = YOLO('yolov8n.pt') 
        self.device = 0 if torch.cuda.is_available() else 'cpu'
        print(f"🚀 AI Running on: {torch.cuda.get_device_name(0)}")
        self.cap = cv2.VideoCapture(0)

    def get_frame(self):
        while True:
            success, frame = self.cap.read()
            if not success: break

            results = self.model(frame, device=self.device, stream=True, conf=0.5)
            violation_found = False

            for r in results:
                boxes = r.boxes
                for box in boxes:
                    if int(box.cls[0]) == 0: # Person detected
                        violation_found = True
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
                        cv2.putText(frame, "NO HELMET", (x1, y1-10), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)

            if violation_found:
                try:
                    loop = asyncio.get_event_loop()
                    if loop.is_running():
                        loop.create_task(alert_manager.broadcast_alert("PPE Violation", "Camera-01"))
                except: pass

            ret, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

streamer = VideoStreamer()