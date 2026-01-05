import cv2
from ultralytics import YOLO
import torch
import asyncio
from backend.alert_manager import alert_manager

class VideoStreamer:
    def __init__(self):
        print("--- Loading PPE Model ---")
        # Load YOUR new custom model
        self.model = YOLO('backend/ppe.pt') 
        
        self.device = 0 if torch.cuda.is_available() else 'cpu'
        print(f"🚀 AI Running on: {torch.cuda.get_device_name(0)}")
        
        # Dictionary to map Class IDs to Names (We will verify these live)
        # Usually: 0=Hardhat, 1=Mask, 2=NO-Hardhat, 3=NO-Mask...
        self.class_names = self.model.names 
        print(f"📋 Model Classes: {self.class_names}")

        # RTSP Link (or 0 for Webcam)
        # CHANGE THIS to your CCTV Link if needed
        self.cap = cv2.VideoCapture(0)

    def get_frame(self):
        while True:
            success, frame = self.cap.read()
            if not success: break

            # 1. Run AI Inference
            # conf=0.4 means "Only show if 40% sure"
            results = self.model(frame, device=self.device, stream=True, conf=0.4, verbose=False)
            
            violation_found = False
            violation_zone = "Unknown"

            # 2. Process Detections
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    # Get Class ID (What is it?)
                    cls_id = int(box.cls[0])
                    current_class = self.class_names[cls_id]
                    
                    # Get Coordinates
                    x1, y1, x2, y2 = map(int, box.xyxy[0])

                    # --- LOGIC: CHECK FOR VIOLATIONS ---
                    # We look for classes that contain "NO-" (e.g., "NO-Hardhat")
                    # Note: Different models use different names. We check broadly.
                    
                    is_violation = "no" in current_class.lower() or "without" in current_class.lower()

                    if is_violation:
                        color = (0, 0, 255) # Red for Danger
                        label = f"VIOLATION: {current_class}"
                        violation_found = True
                        violation_zone = "Zone-A"
                    else:
                        color = (0, 255, 0) # Green for Safe
                        label = f"SAFE: {current_class}"

                    # Draw Box & Label
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 3)
                    cv2.putText(frame, label, (x1, y1-10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

            # 3. Trigger Alert (Async)
            if violation_found:
                try:
                    loop = asyncio.get_event_loop()
                    if loop.is_running():
                        loop.create_task(alert_manager.broadcast_alert("PPE Missing", violation_zone))
                except: pass

            # 4. Encode Frame
            ret, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

streamer = VideoStreamer()