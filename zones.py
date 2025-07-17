# # zones.py
# import json
# import os
# import numpy as np
# import cv2
# from shapely.geometry import Polygon, Point

# def load_zones(zones_path='zones.json'):
#     if not os.path.exists(zones_path):
#         raise FileNotFoundError("❌ zones.json not found. Run draw_zones.py first.")
#     with open(zones_path, 'r') as f:
#         zones = json.load(f)
#     zone_polygons = [Polygon(z['points']) for z in zones]
#     zone_labels = [z['label'] for z in zones]
#     return zones, zone_polygons, zone_labels

# def draw_zones_on_frame(frame, zones):
#     for zone in zones:
#         pts = np.array(zone['points'], np.int32)
#         cv2.polylines(frame, [pts], isClosed=True, color=(255, 0, 0), thickness=2)
#         label_pos = tuple(pts[0])
#         cv2.putText(frame, zone['label'], label_pos, cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

# def get_object_zone(point, zone_polygons, zone_labels):
#     for poly, label in zip(zone_polygons, zone_labels):
#         if poly.contains(Point(point)):
#             return label
#     return None








# zones.py
import json
import os
import numpy as np
import cv2
from shapely.geometry import Polygon, Point

def load_zones(zones_path='zones.json'):
    if not os.path.exists(zones_path):
        raise FileNotFoundError("❌ zones.json not found. Run draw_zones.py or draw_zones_gui.py first.")
    with open(zones_path, 'r') as f:
        zones = json.load(f)
    zone_polygons = [Polygon(z['points']) for z in zones]
    zone_labels = [z['label'] for z in zones]
    return zones, zone_polygons, zone_labels

def draw_zones_on_frame(frame, zones):
    for zone in zones:
        pts = np.array(zone['points'], np.int32)
        cv2.polylines(frame, [pts], isClosed=True, color=(255, 0, 0), thickness=2)
        label_pos = tuple(pts[0])
        cv2.putText(frame, zone['label'], label_pos, cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

def get_object_zone(point, zone_polygons, zone_labels):
    for poly, label in zip(zone_polygons, zone_labels):
        if poly.contains(Point(point)):
            return label
    return None
