

# import cv2
# import json
# import numpy as np
# from datetime import datetime
# from ultralytics import YOLO
# from sort import Sort
# from shapely.geometry import Point, Polygon
# import csv
# import os

# # -----------------------------
# # 1. Load zone definitions
# # -----------------------------
# zones_path = 'zones.json'
# if not os.path.exists(zones_path):
#     print("❌ zones.json not found. Please run draw_zones.py first to define zones.")
#     exit()

# with open(zones_path, 'r') as f:
#     zones = json.load(f)

# zone_polygons = [Polygon(z['points']) for z in zones]
# zone_labels = [z['label'] for z in zones]

# # -----------------------------
# # 2. Initialize YOLO model & SORT tracker
# # -----------------------------
# model_path = 'models/yolov8n.pt'
# if not os.path.exists(model_path):
#     print("❌ YOLO model not found at 'models/yolov8n.pt'. Please download from Ultralytics.")
#     exit()

# model = YOLO(model_path)
# tracker = Sort()

# # -----------------------------
# # 3. Prepare logging system
# # -----------------------------
# os.makedirs('logs', exist_ok=True)
# log_file = open('logs/events.csv', 'w', newline='')
# log_writer = csv.writer(log_file)
# log_writer.writerow(['timestamp', 'object_id', 'zone', 'event'])

# object_zones = {}  # Track last known zone for each object
# recent_events = []  # List to show latest 5 events in overlay
# max_display_events = 5

# # -----------------------------
# # 4. Load video for processing
# # -----------------------------
# video_path = 'test_videos/sample2.mp4'
# if not os.path.exists(video_path):
#     print(f"❌ Could not find test video at: {video_path}")
#     exit()

# cap = cv2.VideoCapture(video_path)
# if not cap.isOpened():
#     print(f"❌ Could not open video: {video_path}")
#     exit()

# cv2.namedWindow("Zone Monitor", cv2.WINDOW_NORMAL)
# cv2.resizeWindow("Zone Monitor", 1280, 720)

# print("🔍 Press 'q' to quit at any time.")

# # -----------------------------
# # 5. Main processing loop
# # -----------------------------
# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     # --- Object Detection ---
#     results = model(frame, verbose=False)[0]
#     detections = []
#     for r in results.boxes.data:
#         x1, y1, x2, y2, score, cls = r.tolist()
#         if int(cls) in [0, 2, 5, 7]:  # person, car, bus, truck
#             detections.append([x1, y1, x2, y2, score])

#     # --- Object Tracking ---
#     if len(detections) > 0:
#         tracked_objects = tracker.update(np.array(detections))
#     else:
#         tracked_objects = []

#     # --- Draw Zones ---
#     for zone in zones:
#         pts = np.array(zone['points'], np.int32)
#         cv2.polylines(frame, [pts], isClosed=True, color=(255, 0, 0), thickness=2)
#         label_pos = tuple(pts[0])
#         cv2.putText(frame, zone['label'], label_pos, cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

#     # --- Process Each Tracked Object ---
#     for obj in tracked_objects:
#         x1, y1, x2, y2, obj_id = obj[:5]
#         center = ((x1 + x2) / 2, (y1 + y2) / 2)
#         point = Point(center)
#         current_zone = None

#         # Determine if object is in a zone
#         for poly, label in zip(zone_polygons, zone_labels):
#             if poly.contains(point):
#                 current_zone = label
#                 break

#         last_zone = object_zones.get(obj_id)

#         if current_zone != last_zone:
#             event_type = 'entry' if current_zone else 'exit'
#             event_zone = current_zone if current_zone else last_zone

#             timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#             log_writer.writerow([timestamp, int(obj_id), event_zone, event_type])
#             print(f"[EVENT] Object {int(obj_id)} {event_type} in {event_zone}")

#             # Add to recent events for overlay
#             overlay_msg = f"[{timestamp.split()[1]}] ID:{int(obj_id)} {event_type.upper()} {event_zone}"
#             recent_events.insert(0, overlay_msg)
#             if len(recent_events) > max_display_events:
#                 recent_events.pop()

#         # Update zone memory
#         if current_zone:
#             object_zones[obj_id] = current_zone
#         elif obj_id in object_zones:
#             del object_zones[obj_id]

#         # Draw object bounding box and ID
#         cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
#         cv2.putText(frame, f'ID:{int(obj_id)}', (int(x1), int(y1) - 10),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

#     # --- Display Event Overlay ---
#     y0, dy = 30, 25
#     for i, line in enumerate(recent_events):
#         y = y0 + i * dy
#         cv2.putText(frame, line, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

#     # --- Show Frame ---
#     cv2.imshow("Zone Monitor", frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         print("🛑 Quitting...")
#         break

# # -----------------------------
# # 6. Cleanup
# # -----------------------------
# log_file.close()
# cap.release()
# cv2.destroyAllWindows()















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
