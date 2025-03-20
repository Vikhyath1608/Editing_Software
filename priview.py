import os
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from moviepy.editor import VideoFileClip
import threading

# Initialize Tkinter
root = tk.Tk()
root.title("🎥 Video Editor with Preview")
root.geometry("500x700")
root.configure(bg="#2c3e50")

# -----------------------
# 🎨 Preview Filter Feature
# -----------------------
def preview_filter():
    input_file = filedialog.askopenfilename(title="Select Video File")
    if not input_file:
        return
    
    # Ask user to choose a filter
    filter_type = simpledialog.askstring("Filter", "Choose filter (grayscale, blur, sepia)")
    
    if filter_type not in ["grayscale", "blur", "sepia"]:
        messagebox.showerror("Error", "Invalid filter. Choose grayscale, blur, or sepia.")
        return

    def process_preview():
        try:
            # Load video
            clip = VideoFileClip(input_file).subclip(0, min(5, VideoFileClip(input_file).duration))  # Short preview (5s max)
            
            # Apply filter
            if filter_type == "grayscale":
                clip = clip.fx(vfx.blackwhite)
            elif filter_type == "blur":
                clip = clip.fx(vfx.gaussian_blur, sigma=5)
            elif filter_type == "sepia":
                clip = clip.fx(vfx.colorx, 0.7)  # Approximate sepia effect
            
            # Show preview in a new window
            preview_window = tk.Toplevel(root)
            preview_window.title("🎥 Preview")
            preview_window.geometry("400x300")
            
            label = tk.Label(preview_window, text="Playing preview...", font=("Arial", 14))
            label.pack(pady=10)
            
            clip.preview()  # Play preview
            preview_window.destroy()  # Close window after preview
        except Exception as e:
            messagebox.showerror("Error", f"Preview failed: {e}")

    threading.Thread(target=process_preview, daemon=True).start()

# -----------------------
# 🎨 Apply Filter and Save
# -----------------------
def apply_filter():
    input_file = filedialog.askopenfilename(title="Select Video File")
    if not input_file:
        return
    
    # Ask user to choose a filter
    filter_type = simpledialog.askstring("Filter", "Choose filter (grayscale, blur, sepia)")
    
    output_file = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])

    if filter_type and output_file:
        command_map = {
            "grayscale": "format=gray",
            "blur": "gblur=sigma=10",
            "sepia": "colorchannelmixer=.393:.769:.189:.349:.686:.168:.272:.534:.131"
        }
        if filter_type not in command_map:
            messagebox.showerror("Error", "Invalid filter. Choose grayscale, blur, or sepia.")
            return
        
        command = f'ffmpeg -i "{input_file}" -vf "{command_map[filter_type]}" "{output_file}"'
        os.system(command)  # Run FFmpeg command
        messagebox.showinfo("Success", f"Filter applied successfully: {output_file}")

# -----------------------
# 🎥 GUI Buttons
# -----------------------
tk.Button(root, text="Preview Filter", command=preview_filter, bg="#3498db", fg="white", padx=5, pady=5).pack(pady=10)
tk.Button(root, text="Apply Filter & Save", command=apply_filter, bg="#1abc9c", fg="white", padx=5, pady=5).pack(pady=10)

# Run Tkinter Main Loop
root.mainloop()
