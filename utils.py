# utils.py
import os
import csv
from datetime import datetime
import cv2

def setup_logging(log_dir='logs', filename='events.csv'):
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, filename)
    log_file = open(log_path, 'w', newline='')
    writer = csv.writer(log_file)
    writer.writerow(['timestamp', 'object_id', 'zone', 'event'])
    return log_file, writer

def log_event(writer, obj_id, zone, event_type):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    writer.writerow([timestamp, int(obj_id), zone, event_type])
    return f"[{timestamp.split()[1]}] ID:{int(obj_id)} {event_type.upper()} {zone}"

def draw_object(frame, obj_id, x1, y1, x2, y2):
    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
    cv2.putText(frame, f'ID:{int(obj_id)}', (int(x1), int(y1) - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

def draw_event_overlay(frame, events, y0=30, dy=25):
    for i, line in enumerate(events[:5]):
        y = y0 + i * dy
        cv2.putText(frame, line, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
