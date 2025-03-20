import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import subprocess
import threading

# Initialize Tkinter
root = tk.Tk()
root.title("🎥 Video Editor with Progress Bar")
root.geometry("500x700")
root.configure(bg="#2c3e50")

# Progress Bar Widget
progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="indeterminate")
progress.pack(pady=10)

# Function to Run FFmpeg in Background
def run_ffmpeg_command(command):
    def worker():
        try:
            progress.start()  # Start progress bar
            subprocess.run(command, check=True, shell=True)
            messagebox.showinfo("Success", "Operation completed successfully!")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"FFmpeg error: {e}")
        finally:
            progress.stop()  # Stop progress bar
    
    threading.Thread(target=worker, daemon=True).start()

# Example Feature: Trim Video with Progress Bar
def trim_video():
    input_file = filedialog.askopenfilename(title="Select Video File")
    if not input_file:
        return
    start_time = simpledialog.askstring("Start Time", "Enter start time (HH:MM:SS)")
    end_time = simpledialog.askstring("End Time", "Enter end time (HH:MM:SS)")
    output_file = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
    
    if start_time and end_time and output_file:
        command = f'ffmpeg -i "{input_file}" -ss {start_time} -to {end_time} -c copy "{output_file}"'
        run_ffmpeg_command(command)

# Button to Trigger Trim Video Function
tk.Button(root, text="Trim Video", command=trim_video, bg="#1abc9c", fg="white", padx=5, pady=5).pack(pady=10)

# Run Tkinter Main Loop
root.mainloop()
