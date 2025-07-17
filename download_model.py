# download_model.py
from ultralytics import YOLO

YOLO('yolov8n.pt')  # This will download the model to ~/.cache
