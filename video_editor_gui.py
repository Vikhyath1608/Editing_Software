import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from moviepy.editor import *
import subprocess


# Run FFmpeg command
def run_ffmpeg_command(command):
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"FFmpeg error: {e}")


# -----------------------
# ✂️ 1. Trim Video
# -----------------------
def trim_video():
    input_file = filedialog.askopenfilename(title="Select Video File")
    if not input_file:
        return
    start_time = simpledialog.askstring("Start Time", "Enter start time (HH:MM:SS)")
    end_time = simpledialog.askstring("End Time", "Enter end time (HH:MM:SS)")
    output_file = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
    if start_time and end_time and output_file:
        command = f"ffmpeg -i \"{input_file}\" -ss {start_time} -to {end_time} -c copy \"{output_file}\""
        run_ffmpeg_command(command)
        messagebox.showinfo("Success", f"Video trimmed successfully: {output_file}")


# -----------------------
# 🎬 2. Merge Videos
# -----------------------
def merge_videos():
    input_files = filedialog.askopenfilenames(title="Select Videos to Merge")
    if not input_files:
        return
    output_file = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
    if output_file:
        with open("file_list.txt", "w") as f:
            for file in input_files:
                f.write(f"file '{file}'\n")
        command = f"ffmpeg -f concat -safe 0 -i file_list.txt -c copy \"{output_file}\""
        run_ffmpeg_command(command)
        os.remove("file_list.txt")
        messagebox.showinfo("Success", f"Videos merged successfully: {output_file}")


# -----------------------
# 🎨 3. Apply Filters
# -----------------------
def apply_filter():
    input_file = filedialog.askopenfilename(title="Select Video File")
    if not input_file:
        return
    filter_type = simpledialog.askstring("Filter", "Choose filter (grayscale, blur, sepia)")
    output_file = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])

    filter_map = {
        "grayscale": "format=gray",
        "blur": "gblur=sigma=10",
        "sepia": "colorchannelmixer=.393:.769:.189:.349:.686:.168:.272:.534:.131"
    }

    if filter_type and filter_type in filter_map and output_file:
        command = f"ffmpeg -i \"{input_file}\" -vf {filter_map[filter_type]} \"{output_file}\""
        run_ffmpeg_command(command)
        messagebox.showinfo("Success", f"Filter applied successfully: {output_file}")


# -----------------------
# ✏️ 4. Add Text/Watermark
# -----------------------
def add_text():
    input_file = filedialog.askopenfilename(title="Select Video File")
    if not input_file:
        return
    text = simpledialog.askstring("Add Text", "Enter the text to overlay")
    output_file = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])

    if text and output_file:
        video = VideoFileClip(input_file)
        txt_clip = TextClip(text, fontsize=50, color='white').set_duration(video.duration).set_position('bottom').set_opacity(0.7)
        video_with_text = CompositeVideoClip([video, txt_clip])
        video_with_text.write_videofile(output_file, codec='libx264')
        messagebox.showinfo("Success", f"Text added successfully: {output_file}")


# -----------------------
# ⏩ 5. Change Video Speed
# -----------------------
def change_speed():
    input_file = filedialog.askopenfilename(title="Select Video File")
    if not input_file:
        return
    speed_factor = simpledialog.askfloat("Speed Factor", "Enter speed factor (e.g., 2.0 for 2x speed, 0.5 for half speed)")
    output_file = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])

    if speed_factor and output_file:
        command = f"ffmpeg -i \"{input_file}\" -filter:v \"setpts={1/float(speed_factor)}*PTS\" \"{output_file}\""
        run_ffmpeg_command(command)
        messagebox.showinfo("Success", f"Speed adjusted successfully: {output_file}")


# -----------------------
# 🔄 6. Convert Video Format
# -----------------------
def convert_format():
    input_file = filedialog.askopenfilename(title="Select Video File")
    if not input_file:
        return
    output_format = simpledialog.askstring("Convert Format", "Enter output format (mp4, avi, mkv, mov)")
    output_file = filedialog.asksaveasfilename(defaultextension=f".{output_format}", filetypes=[(f"{output_format.upper()} files", f"*.{output_format}")])

    if output_file:
        command = f"ffmpeg -i \"{input_file}\" \"{output_file}\""
        run_ffmpeg_command(command)
        messagebox.showinfo("Success", f"Video converted successfully: {output_file}")


# -----------------------
# 🎧 7. Extract Audio from Video
# -----------------------
def extract_audio():
    input_file = filedialog.askopenfilename(title="Select Video File")
    if not input_file:
        return
    output_file = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
    if output_file:
        command = f"ffmpeg -i \"{input_file}\" -q:a 0 -map a \"{output_file}\""
        run_ffmpeg_command(command)
        messagebox.showinfo("Success", f"Audio extracted successfully: {output_file}")


# -----------------------
# 🎵 8. Add Background Music
# -----------------------
def add_background_music():
    video_file = filedialog.askopenfilename(title="Select Video File")
    if not video_file:
        return
    audio_file = filedialog.askopenfilename(title="Select Audio File")
    if not audio_file:
        return
    output_file = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
    if output_file:
        command = f"ffmpeg -i \"{video_file}\" -i \"{audio_file}\" -c:v copy -map 0:v:0 -map 1:a:0 -shortest \"{output_file}\""
        run_ffmpeg_command(command)
        messagebox.showinfo("Success", f"Background music added successfully: {output_file}")


# -----------------------
# 🎞️ 9. Create GIF from Video
# -----------------------
def create_gif():
    input_file = filedialog.askopenfilename(title="Select Video File")
    if not input_file:
        return
    output_file = filedialog.asksaveasfilename(defaultextension=".gif", filetypes=[("GIF files", "*.gif")])
    if output_file:
        command = f"ffmpeg -i \"{input_file}\" -vf \"fps=10,scale=320:-1:flags=lanczos\" \"{output_file}\""
        run_ffmpeg_command(command)
        messagebox.showinfo("Success", f"GIF created successfully: {output_file}")


# -----------------------
# 📏 10. Resize/Scale Video
# -----------------------
def resize_video():
    input_file = filedialog.askopenfilename(title="Select Video File")
    if not input_file:
        return
    width = simpledialog.askinteger("Width", "Enter new width")
    height = simpledialog.askinteger("Height", "Enter new height")
    output_file = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])

    if width and height and output_file:
        command = f"ffmpeg -i \"{input_file}\" -vf scale={width}:{height} \"{output_file}\""
        run_ffmpeg_command(command)
        messagebox.showinfo("Success", f"Video resized successfully: {output_file}")


# -----------------------
# 🔄 11. Rotate/Flip Video
# -----------------------
def rotate_video():
    input_file = filedialog.askopenfilename(title="Select Video File")
    if not input_file:
        return
    rotation_option = simpledialog.askstring("Rotation", "Choose rotation (90, 180, flipH, flipV)")
    output_file = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])

    rotation_map = {
        "90": "transpose=1",
        "180": "transpose=2,transpose=2",
        "flipH": "hflip",
        "flipV": "vflip"
    }

    if rotation_option and rotation_option in rotation_map and output_file:
        command = f"ffmpeg -i \"{input_file}\" -vf \"{rotation_map[rotation_option]}\" \"{output_file}\""
        run_ffmpeg_command(command)
        messagebox.showinfo("Success", f"Video rotated/flipped successfully: {output_file}")


# -----------------------
# 🖼️ 12. Add Image/Logo Watermark
# -----------------------
def add_image_watermark():
    video_file = filedialog.askopenfilename(title="Select Video File")
    if not video_file:
        return
    image_file = filedialog.askopenfilename(title="Select Image/Logo File")
    if not image_file:
        return
    output_file = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
    if output_file:
        command = f"ffmpeg -i \"{video_file}\" -i \"{image_file}\" -filter_complex \"overlay=10:10\" \"{output_file}\""
        run_ffmpeg_command(command)
        messagebox.showinfo("Success", f"Watermark added successfully: {output_file}")


# -----------------------
# 🔇 13. Mute Audio from Video
# -----------------------
def mute_audio():
    input_file = filedialog.askopenfilename(title="Select Video File")
    if not input_file:
        return
    output_file = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
    if output_file:
        command = f"ffmpeg -i \"{input_file}\" -an \"{output_file}\""
        run_ffmpeg_command(command)
        messagebox.showinfo("Success", f"Audio muted successfully: {output_file}")


# -----------------------
# 🎥 GUI Setup
# -----------------------
root = tk.Tk()
root.title("🎥 All-in-One Video Editor - Ultimate Toolkit")
root.geometry("500x700")
root.configure(bg="#2c3e50")

# Add All Buttons for 19 Features
features = {
    "Trim Video": trim_video,
    "Merge Videos": merge_videos,
    "Apply Filter": apply_filter,
    "Add Text/Watermark": add_text,
    "Change Video Speed": change_speed,
    "Convert Video Format": convert_format,
    "Extract Audio": extract_audio,
    "Add Background Music": add_background_music,
    "Create GIF from Video": create_gif,
    "Resize/Scale Video": resize_video,
    "Rotate/Flip Video": rotate_video,
    "Add Image/Logo Watermark": add_image_watermark,
    "Mute Audio from Video": mute_audio
}

for feature, command in features.items():
    tk.Button(root, text=feature, command=command, bg="#1abc9c", fg="white", padx=5, pady=5).pack(pady=5)

root.mainloop()
#multiple editing functions with video