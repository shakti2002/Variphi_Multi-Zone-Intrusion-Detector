🎯 Real-time Object Detection & Zone Tracking System
A real-time video analytics system that enables:

Drawing custom zones on a video frame using a Tkinter GUI

Detecting objects using YOLOv8

Tracking objects across frames using SORT

Counting and logging object entries/exits inside defined zones

Visualizing and saving the annotated output video

🔧 Project Overview
This project builds a smart object tracking pipeline to:

Draw zones (e.g., entry gates, restricted areas)

Detect and track objects across video frames

Analyze movement with respect to zones

Save results and logs for further insights

🧱 Architecture Components
🔷 1. Frontend GUI (Zone Drawer)
Tool: Tkinter
File: draw_zones_gui.py
Responsibility:

Load the first frame of a video

Allow user to draw polygon zones on the frame

Save zones to zones.json

🔷 2. Object Detection
Tool: Ultralytics YOLOv8
File: Utilized in detection.py
Responsibility:

Detect objects (e.g., persons, vehicles)

Output bounding boxes with class labels and confidence scores

🔷 3. Object Tracking
Algorithm: SORT (Simple Online Realtime Tracking)
File: sort.py
Responsibility:

Track detected objects across frames

Assign unique IDs to objects

Maintain object identity over time

🔷 4. Zone Logic & Analytics
Modules: zones.py, utils.py
Responsibility:

Check if tracked objects enter/exit zones

Maintain entry/exit counters

Save logs with object IDs and timestamps

🔷 5. Main Pipeline
File: detection.py
Responsibility:

Load video, zones, detection, and tracking models

Run full inference pipeline

Visualize bounding boxes, zones, and counts

Output processed video



---

## 📁 Folder Structure

object_zone_tracking_project/
├── detection.py # Main script (detection + tracking + zone logic)
├── sort.py # SORT tracker implementation
├── zones.py # Zone logic and polygon checks
├── utils.py # IOU, logging, helper functions
├── draw_zones_gui.py # Tkinter GUI for polygon zone drawing
├── zones.json # Stores polygon coordinates
├── test_videos/
│ └── sample.mp4 # Input video
├── outputs/
│ └── processed_video.mp4 # Output video
├── requirements.txt # Required Python packages



---

## 📌 How It All Works

### ✅ Step 1: Draw Zones
1. Run the GUI:
   ```bash
   python draw_zones_gui.py
