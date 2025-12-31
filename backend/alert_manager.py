from fastapi import WebSocket
from datetime import datetime
from backend.database import db

class AlertSystem:
    def __init__(self):
        self.active_connections = []
        self.last_alert_time = 0
        self.cooldown = 4

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast_alert(self, violation_type, zone):
        current_time = datetime.now().timestamp()
        if (current_time - self.last_alert_time) < self.cooldown:
            return

        self.last_alert_time = current_time
        
        alert_data = {
            "type": violation_type,
            "zone": zone,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        }

        await db["alerts"].insert_one(alert_data.copy())

        if "_id" in alert_data: del alert_data["_id"]
        
        for connection in self.active_connections:
            try:
                await connection.send_json(alert_data)
            except:
                self.disconnect(connection)

alert_manager = AlertSystem()