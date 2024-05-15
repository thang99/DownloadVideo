import tkinter as tk
from tkinter import filedialog
from pytube import YouTube
import os
from moviepy.editor import VideoFileClip
from threading import Thread

downloaded_videos = []

def browse_directory():
    global download_path
    download_path = filedialog.askdirectory()
    update_downloaded_videos_list()

def download_video():
    url = url_entry.get()
    try:
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        filename = stream.default_filename
        stream.download(output_path=download_path)
        status_label.config(text="Download completed!", fg="green")
        downloaded_videos.append(filename)
        update_downloaded_videos_list()
    except Exception as e:
        status_label.config(text="Error: " + str(e), fg="red")

def update_downloaded_videos_list():
    downloaded_videos_listbox.delete(0, tk.END)
    if not os.path.isdir(download_path):
        status_label.config(text="Invalid directory!", fg="red")
        return
    videos = [f for f in os.listdir(download_path) if os.path.isfile(os.path.join(download_path, f)) and f.endswith(('.mp4', '.mkv', '.avi', '.flv'))]
    for video in videos:
        downloaded_videos_listbox.insert(tk.END, video)

def play_video():
    selected_index = downloaded_videos_listbox.curselection()
    if selected_index:
        selected_video = downloaded_videos_listbox.get(selected_index)
        video_path = os.path.join(download_path, selected_video)
        Thread(target=play_video_thread, args=(video_path,)).start()

def play_video_thread(video_path):
    try:
        video = VideoFileClip(video_path)
        video.preview()
    except Exception as e:
        status_label.config(text="Error: " + str(e), fg="red")

# Tạo cửa sổ chính
root = tk.Tk()
root.title("YouTube Video Downloader")
root.geometry("600x400")

# Tạo nhãn và ô nhập URL
url_label = tk.Label(root, text="Enter YouTube URL:", font=("Arial", 12))
url_label.pack(pady=(20,5))

url_entry = tk.Entry(root, width=50, font=("Arial", 12))
url_entry.pack()

# Tạo nút chọn thư mục
browse_button = tk.Button(root, text="Browse", command=browse_directory, font=("Arial", 12))
browse_button.pack(pady=5)

# Tạo nút tải xuống
download_button = tk.Button(root, text="Download", command=download_video, font=("Arial", 12))
download_button.pack(pady=5)

# Tạo cảnh báo nhãn
status_label = tk.Label(root, text="", font=("Arial", 12))
status_label.pack(pady=10)

# Tạo nhãn danh sách video đã tải
downloaded_videos_label = tk.Label(root, text="Downloaded Videos:", font=("Arial", 12))
downloaded_videos_label.pack(pady=(20,5))

# Tạo danh sáchbox cho video đã tải
downloaded_videos_listbox = tk.Listbox(root, height=5, width=70, font=("Arial", 12))
downloaded_videos_listbox.pack(pady=5)

# Tạo nút phát video
play_button = tk.Button(root, text="Play", command=play_video, font=("Arial", 12))
play_button.pack(pady=5)

root.mainloop()
