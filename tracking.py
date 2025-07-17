# tracking.py
import numpy as np
from sort import Sort

def initialize_tracker():
    return Sort()

def update_tracker(tracker, detections):
    if len(detections) > 0:
        return tracker.update(np.array(detections))
    else:
        return []
