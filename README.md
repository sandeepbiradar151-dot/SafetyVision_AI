# SafetyVision_AI

Lightweight safety-vision demo combining a FastAPI backend (YOLOv8) and a Vite + React frontend.

This README explains how to set up and run the project after cloning the repository.

## Overview

- Backend: `backend/` — FastAPI app that streams webcam frames and broadcasts alerts via WebSocket.
- Frontend: `frontend/` — React + Vite app that connects to the backend to display video and alerts.
- Note: The model weights (`yolov8n.pt`) and any large dataset/model files are intentionally gitignored and must be placed manually (or managed with Git LFS).

## Requirements

- Windows (instructions use PowerShell) or any OS with Python 3.8+ and Node.js.
- Python 3.8+ (3.10/3.11 recommended)
- Node 18+ and npm
- A webcam for live video streaming (or change camera index in `backend/camera_core.py`).
- Optional: CUDA-enabled GPU and a matching PyTorch build for faster inference.

## Quick setup (recommended)

1. Clone the repo:

```powershell
git clone https://github.com/sandeepbiradar151-dot/SafetyVision_AI.git
cd SafetyVision_AI
```

2. Backend (Python)

- Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate
# On Linux / macOS: source .venv/bin/activate
```

- Install dependencies. If a `backend/requirements.txt` is available, use it. Otherwise install the minimal packages:

```powershell
pip install --upgrade pip
pip install fastapi uvicorn python-dotenv motor opencv-python ultralytics
# NOTE: install PyTorch separately according to your system and CUDA: https://pytorch.org/get-started/locally/
# For CPU-only, one option is:
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

- Create a `.env` file in the project root (or set environment variables). At minimum set your MongoDB connection string:

```
MONGO_URI=mongodb://localhost:27017
```

- Place the YOLOv8 weights file `yolov8n.pt` in the project root. This repository intentionally excludes the weights. You can download official weights from Ultralytics or place your custom model.

3. Frontend (Node)

```powershell
cd frontend
npm install
npm run dev
# By default Vite will serve on http://localhost:5173
```

4. Run the backend

In a new PowerShell (with the Python venv activated):

```powershell
cd ..\
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
# Backend API will be available at http://localhost:8000
# Video stream endpoint: http://localhost:8000/video_feed
# WebSocket alerts endpoint: ws://localhost:8000/ws/alerts
```

5. Open the frontend app (the Vite dev server). The frontend should connect to the backend endpoints listed above.

## Verifying GPU (optional)

Run the provided diagnostic script:

```powershell
python check_gpu.py
```

If you want to use GPU inference, install a PyTorch build that matches your CUDA version. See https://pytorch.org/get-started/locally/ for the right command.

## Notes & recommendations

- Large model files (e.g., `yolov8n.pt`) are ignored by git. If you want to version them use Git LFS:

```powershell
git lfs install
git lfs track "yolov8n.pt"
git add .gitattributes
```

- Camera index: The backend opens `cv2.VideoCapture(0)`. Change `0` to another index if your camera is different or use a video file for testing.
- MongoDB: The project uses Motor (async MongoDB). Ensure `MONGO_URI` points to a running MongoDB instance.
- If you see errors about CUDA device names, it's safe to fall back to CPU by ensuring PyTorch is installed with CPU-only wheels or by modifying `camera_core.py` to avoid calling `torch.cuda.get_device_name(0)` when CUDA is not available.

## Troubleshooting

- If the frontend can't connect to the backend, check CORS (FastAPI allows all origins in `backend/main.py`) and correct ports.
- If OpenCV can't open the camera, close other apps using it or change the camera index.
- If dependencies fail, check Python version and reinstall packages in a fresh virtualenv.

## Contributing

Feel free to open issues or PRs. Suggested small improvements:
- Add a `backend/requirements.txt` with pinned versions.
- Add Dockerfiles for reproducible deployment.
- Add GitHub Actions for CI.

---

If you'd like, I can also:
- create a `backend/requirements.txt` listing detected imports,
- set up Git LFS tracking for `yolov8n.pt`, or
- add a small Docker Compose to run the app + MongoDB locally.
