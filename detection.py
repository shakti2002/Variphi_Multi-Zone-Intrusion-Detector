# detection.py
from ultralytics import YOLO
import os

def load_model(model_path='models/yolov8n.pt'):
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"❌ YOLO model not found at {model_path}")
    return YOLO(model_path)

def detect_objects(model, frame):
    results = model(frame, verbose=False)[0]
    detections = []

    for r in results.boxes.data:
        x1, y1, x2, y2, score, cls = r.tolist()
        if int(cls) in [0, 2, 5, 7]:  # person, car, bus, truck
            detections.append([x1, y1, x2, y2, score])

    return detections
