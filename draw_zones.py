
import cv2
import json
import os
import numpy as np
from tkinter import simpledialog, Tk

# Global state
zones = []
current_points = []
drawing_enabled = False  # Toggle with 'd'
frame = None

def mouse_callback(event, x, y, flags, param):
    global current_points, drawing_enabled

    if not drawing_enabled:
        return

    if event == cv2.EVENT_LBUTTONDOWN:
        current_points.append((x, y))

def draw_polygons(image, zones, current_points):
    # Draw existing zones
    for zone in zones:
        pts = zone["points"]
        if len(pts) >= 3:
            cv2.polylines(image, [np.array(pts, np.int32)], True, (0, 255, 0), 2)
            # Draw label
            x, y = pts[0]
            cv2.putText(image, zone["label"], (x + 5, y - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Draw current zone being drawn
    if len(current_points) >= 2:
        cv2.polylines(image, [np.array(current_points, np.int32)], False, (0, 0, 255), 2)

    for point in current_points:
        cv2.circle(image, point, 5, (0, 0, 255), -1)

    return image

def prompt_zone_name():
    root = Tk()
    root.withdraw()
    name = simpledialog.askstring("Zone Name", "Enter a name for this zone:")
    root.destroy()
    return name

def main():
    global frame, current_points, zones, drawing_enabled

    import numpy as np  # Required for polygon drawing

    video_path = "test_videos/sample2.mp4"
    if not os.path.exists(video_path):
        print(f"❌ Video not found: {video_path}")
        return

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("❌ Could not open video.")
        return

    window_name = "Draw Zones - Press 'd' to toggle drawing | 'n' to name | 's' to save | 'q' to quit"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 1280, 720)
    cv2.setMouseCallback(window_name, mouse_callback)

    print("🖱️ Left-click to select polygon points.")
    print("🎥 Press 'd' to toggle drawing mode ON/OFF.")
    print("✅ Press 'n' to name and save the current zone.")
    print("💾 Press 's' to save all zones to zones.json.")
    print("❌ Press 'q' to quit.")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("🎬 End of video.")
            break

        display = draw_polygons(frame.copy(), zones, current_points)
        cv2.imshow(window_name, display)
        key = cv2.waitKey(30) & 0xFF

        if key == ord('d'):
            drawing_enabled = not drawing_enabled
            print(f"🖊️ Drawing mode {'enabled' if drawing_enabled else 'disabled'}.")

        elif key == ord('n'):
            if len(current_points) >= 3:
                zone_name = prompt_zone_name()
                if zone_name:
                    zones.append({
                        "label": zone_name,
                        "points": current_points.copy()
                    })
                    print(f"✅ Zone '{zone_name}' added.")
                    current_points.clear()
            else:
                print("⚠️ At least 3 points needed to form a polygon.")

        elif key == ord('s'):
            with open("zones.json", "w") as f:
                json.dump(zones, f, indent=2)
            print("💾 zones.json saved.")

        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
