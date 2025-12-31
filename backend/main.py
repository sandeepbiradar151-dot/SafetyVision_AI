from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from backend.database import check_db
from backend.camera_core import streamer
from backend.alert_manager import alert_manager

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await check_db()

@app.get("/video_feed")
def video_feed():
    return StreamingResponse(streamer.get_frame(), media_type='multipart/x-mixed-replace; boundary=frame')

@app.websocket("/ws/alerts")
async def websocket_endpoint(websocket: WebSocket):
    await alert_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        alert_manager.disconnect(websocket)