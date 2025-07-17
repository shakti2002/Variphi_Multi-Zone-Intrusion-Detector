# 🎯 Real-time Object Detection and Zone Tracking System

## 🔧 Project Overview

This project is a **real-time video analytics system** that:

- Allows **drawing custom polygonal zones** on video frames via a GUI (Tkinter)
- Uses **YOLOv8** for real-time object detection
- Applies the **SORT tracking algorithm** to maintain object identities across frames
- Detects **entry/exit** events in predefined zones
- Logs zone-wise analytics like object count, IDs, and timestamps
- Outputs **annotated videos** with zone tracking overlays

---

## 🧱 Architecture Diagram


## 🧱 Architecture Components

### 🔷 1. Frontend GUI (Zone Drawer)
- **Tool:** Tkinter
- **File:** `draw_zones_gui.py`

**Responsibilities:**
- Load the first frame of a video
- Let the user draw custom polygon zones
- Save zones to `zones.json`

---

### 🔷 2. Object Detection
- **Tool:** Ultralytics YOLOv8
- **File:** Integrated into `detection.py`

**Responsibilities:**
- Detect objects in video frames
- Output bounding boxes, classes, and confidence scores

---

### 🔷 3. Object Tracking
- **Algorithm:** SORT (Simple Online Realtime Tracking)
- **File:** `sort.py`

**Responsibilities:**
- Assign consistent IDs to objects
- Track objects across frames
- Output tracked bounding boxes with IDs

---

### 🔷 4. Zone Checking & Analytics
- **Files:** `zones.py`, `utils.py`

**Responsibilities:**
- Check if tracked objects enter or exit custom zones
- Maintain counters per zone
- Log analytics (entry/exit logs with timestamps)

---

### 🔷 5. Main Pipeline
- **File:** `detection.py`

**Responsibilities:**
- Load the video and zones
- Run detection, tracking, and zone analysis
- Draw annotated frames and save processed output video

---

## 📁 Folder Structure

```bash
object_zone_tracking_project/
├── detection.py               # Main pipeline to run detection, tracking, zone check
├── sort.py                    # SORT algorithm implementation
├── zones.json                 # Saved zones from GUI
├── draw_zones_gui.py          # GUI to draw zones and save them
├── zones.py                   # Polygon logic for zone entry/exit checks
├── utils.py                   # Helper functions for IOU, drawing, logging
├── test_videos/
│   └── sample.mp4             # Sample video for testing
├── outputs/
│   └── processed_video.mp4    # Annotated video output
├── requirements.txt           # Required Python packages

```

### ✅ How It Works

### 🎨 Step 1: Draw Zones

```bash
python draw_zones_gui.py
```

Select a video from the file dialog.

Click on the frame to draw a polygon zone.

Press s to save the zone in zones.json.

### 🚀 Step 2: Run Detection + Tracking
```bash
python detection.py
```
This will:

Load YOLOv8.

Load zones from zones.json.

Detect and track objects using the SORT algorithm.

Monitor object entry and exit across zones.

Save the annotated video in outputs/processed_video.mp4.

##  Use of Each File

| File                | Purpose                                                            |
| ------------------- | ------------------------------------------------------------------ |
| `detection.py`      | Main runner script integrating detection, tracking, and zone logic |
| `draw_zones_gui.py` | GUI tool for loading frames and drawing custom detection zones     |
| `zones.json`        | Stores user-defined zones as polygons                              |
| `zones.py`          | Logic to verify if tracked objects fall inside defined zones       |
| `sort.py`           | Implementation of the SORT tracking algorithm                      |
| `utils.py`          | Drawing helpers, IOU calculations, and utility functions           |
| `test_videos/`      | Folder for storing input videos                                    |
| `outputs/`          | Output folder where processed results are saved                    |
| `requirements.txt`  | List of required Python packages                                   |


## ▶️ How to Run the Project

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```
### Step 2: Draw Custom Zones
```bash
python draw_zones_gui.py
```
 OR 
```bash
python draw_zones.py
```
Click on the video frame to draw your polygon zone.

Press s to save it to zones.json.

 ### Step 3: Run Detection + Tracking
```bash
python detection.py
```
The processed output video will be saved as:
outputs/processed_video.mp4

## Tools & Dependencies

| Component          | Library / Tool      |
| ------------------ | ------------------- |
| GUI Interface      | Tkinter             |
| Object Detection   | Ultralytics YOLOv8  |
| Object Tracking    | SORT                |
| Zone Monitoring    | OpenCV (cv2)        |
| Visualization      | OpenCV + `utils.py` |
| Data Saving Format | JSON, CSV           |

 ## Final Output

✅ Processed video saved at: outputs/processed_video.mp4

📄 Optional logs of object entry/exit per zone in CSV/JSON format

🔁 Zones are reusable via zones.json

