

import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import cv2
from PIL import Image, ImageTk
import json


class ZoneDrawerGUI:
    def __init__(self, video_path):
        self.video_path = video_path
        self.points = []
        self.zones = []
        self.drawing = True

        self.cap = cv2.VideoCapture(self.video_path)
        if not self.cap.isOpened():
            raise Exception("Failed to read video")

        # Read the first frame to get dimensions
        success, frame = self.cap.read()
        if not success:
            raise Exception("Failed to read video frame")

        self.orig_height, self.orig_width = frame.shape[:2]
        self.display_width = 960
        self.display_height = int(self.orig_height * (self.display_width / self.orig_width))

        # Setup Tkinter
        self.root = tk.Tk()
        self.root.title("Draw Zones - GUI")

        self.canvas = tk.Canvas(self.root, width=self.display_width, height=self.display_height)
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.on_click)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(fill="x")

        tk.Button(btn_frame, text="Finish Zone", command=self.finish_zone).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Undo Point", command=self.undo_point).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Save Zones", command=self.save_zones).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Exit", command=self.quit_app).pack(side="right", padx=5)

        self.update_video_frame()
        self.root.mainloop()

    def update_video_frame(self):
        if self.drawing:
            ret, frame = self.cap.read()
            if not ret:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = self.cap.read()

            resized_frame = cv2.resize(frame, (self.display_width, self.display_height))
            self.current_frame = resized_frame.copy()

            # Convert and display frame
            img = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            self.tk_image = ImageTk.PhotoImage(img)
            self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)

            # Redraw points
            self.draw_points()

        self.root.after(30, self.update_video_frame)  # ~33 FPS

    def on_click(self, event):
        scale_x = self.orig_width / self.display_width
        scale_y = self.orig_height / self.display_height
        orig_x = int(event.x * scale_x)
        orig_y = int(event.y * scale_y)

        self.points.append((orig_x, orig_y))

    def draw_points(self):
        self.canvas.delete("zone")
        scale_x = self.display_width / self.orig_width
        scale_y = self.display_height / self.orig_height

        for i in range(len(self.points)):
            x1, y1 = self.points[i]
            x1_disp, y1_disp = int(x1 * scale_x), int(y1 * scale_y)
            self.canvas.create_oval(x1_disp - 3, y1_disp - 3, x1_disp + 3, y1_disp + 3,
                                    fill="red", tags="zone")

            if i > 0:
                x2, y2 = self.points[i - 1]
                x2_disp, y2_disp = int(x2 * scale_x), int(y2 * scale_y)
                self.canvas.create_line(x1_disp, y1_disp, x2_disp, y2_disp,
                                        fill="blue", width=2, tags="zone")

    def finish_zone(self):
        if len(self.points) >= 3:
            # Ask user for label
            zone_label = simpledialog.askstring("Zone Label", "Enter a label for this zone:")
            if not zone_label:
                messagebox.showwarning("No Label", "Zone not saved. Please enter a label.")
                return

            self.zones.append({
                "label": zone_label,
                "points": self.points.copy()
            })
            print(f"[INFO] Zone '{zone_label}' saved.")
            self.points.clear()
            self.canvas.delete("zone")
        else:
            messagebox.showwarning("Not enough points", "A zone needs at least 3 points.")

    def undo_point(self):
        if self.points:
            self.points.pop()

    def save_zones(self):
        with open("zones.json", "w") as f:
            json.dump(self.zones, f, indent=4)
        messagebox.showinfo("Saved", "Zones saved to zones.json.")

    def quit_app(self):
        self.drawing = False
        self.cap.release()
        self.root.quit()


# Run GUI if script is run directly
if __name__ == "__main__":
    file_path = filedialog.askopenfilename(title="Select Video File",
                                           filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv")])
    if file_path:
        ZoneDrawerGUI(file_path)
