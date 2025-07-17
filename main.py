

# main.py
import cv2
import numpy as np

from detection import load_model, detect_objects
from tracking import initialize_tracker, update_tracker
from zones import load_zones, draw_zones_on_frame, get_object_zone
from utils import setup_logging, log_event, draw_object, draw_event_overlay

# 1. Load zones
zones, zone_polygons, zone_labels = load_zones()

# 2. Load model and tracker
model = load_model()
tracker = initialize_tracker()

# 3. Setup logging
log_file, log_writer = setup_logging()
object_zones = {}
recent_events = []

# 4. Load video
video_path = 'test_videos/sample2.mp4'
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    raise RuntimeError(f"❌ Could not open video: {video_path}")

cv2.namedWindow("Zone Monitor", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Zone Monitor", 1280, 720)
print("🔍 Press 'q' to quit at any time.")

# 5. Main loop
while True:
    ret, frame = cap.read()
    if not ret:
        break

    detections = detect_objects(model, frame)
    tracked_objects = update_tracker(tracker, detections)

    draw_zones_on_frame(frame, zones)

    for obj in tracked_objects:
        x1, y1, x2, y2, obj_id = obj[:5]
        center = ((x1 + x2) / 2, (y1 + y2) / 2)
        current_zone = get_object_zone(center, zone_polygons, zone_labels)
        last_zone = object_zones.get(obj_id)

        if current_zone != last_zone:
            event_type = 'entry' if current_zone else 'exit'
            event_zone = current_zone if current_zone else last_zone
            msg = log_event(log_writer, obj_id, event_zone, event_type)
            print(f"[EVENT] {msg}")
            recent_events.insert(0, msg)
            recent_events = recent_events[:5]

        if current_zone:
            object_zones[obj_id] = current_zone
        elif obj_id in object_zones:
            del object_zones[obj_id]

        draw_object(frame, obj_id, x1, y1, x2, y2)

    draw_event_overlay(frame, recent_events)
    cv2.imshow("Zone Monitor", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("🛑 Quitting...")
        break

# 6. Cleanup
log_file.close()
cap.release()
cv2.destroyAllWindows()
