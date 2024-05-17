import tkinter as tk
from tkinter import ttk, filedialog
from pytube import YouTube
from googleapiclient.discovery import build
import os
from moviepy.editor import VideoFileClip
from tkinter import filedialog

API_KEY = "AIzaSyAaNFrAdAI36Y0nTCtrRaeJr5nLus-Gx08"

def download_video(url):
    try:
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        filename = stream.default_filename
        stream.download(output_path=download_path)
        if tab_control.index(tab_control.select()) == 0:
            status_label.config(text="Download completed!", fg="green")
        elif tab_control.index(tab_control.select()) == 1:
            status_label_url.config(text="Download completed!", fg="green")
        update_downloaded_videos_list()
    except Exception as e:
        if tab_control.index(tab_control.select()) == 0:
            status_label.config(text="Error: " + str(e), fg="red")
        elif tab_control.index(tab_control.select()) == 1:
            status_label_url.config(text="Error: " + str(e), fg="red")

def select_video_to_download():
    selected_index = search_results.curselection()
    if selected_index:
        selected_video_title = search_results.get(selected_index)
        query = search_entry.get()
        youtube = build("youtube", "v3", developerKey=API_KEY)
        request = youtube.search().list(
            q=query,
            part="snippet",
            type="video",
            maxResults=10
        )
        response = request.execute()
        for item in response["items"]:
            if item["snippet"]["title"] == selected_video_title:
                selected_video_id = item["id"]["videoId"]
                selected_video_url = f"https://www.youtube.com/watch?v={selected_video_id}"
                download_video(selected_video_url)

def search_youtube():
    query = search_entry.get()
    youtube = build("youtube", "v3", developerKey=API_KEY)
    request = youtube.search().list(
        q=query,
        part="snippet",
        type="video",
        maxResults=10
    )
    response = request.execute()
    search_results.delete(0, tk.END)
    for item in response["items"]:
        search_results.insert(tk.END, item["snippet"]["title"])

def download_from_url():
    url = url_entry.get()
    download_video(url)

def update_downloaded_videos_list():
    try:
        downloaded_videos_listbox.delete(0, tk.END)
        if not os.path.isdir(download_path):
            status_label.config(text="Invalid directory!", fg="red")
            return
        videos = [f for f in os.listdir(download_path) if os.path.isfile(os.path.join(download_path, f)) and f.endswith(('.mp4', '.mkv', '.avi', '.flv'))]
        for video in videos:
            downloaded_videos_listbox.insert(tk.END, video)
    except Exception as e:
        print("Error updating downloaded videos list:", e)

def browse_directory():
    global download_path
    download_path = filedialog.askdirectory()
    update_downloaded_videos_list()
    download_path_label.config(text=f"Download Path: {download_path}")

def play_video():
    selected_index = downloaded_videos_listbox.curselection()
    if selected_index:
        selected_video = downloaded_videos_listbox.get(selected_index)
        video_path = os.path.join(download_path, selected_video)
        try:
            video = VideoFileClip(video_path)                
            video.preview()
        except Exception as e:
            status_label.config(text="Error: " + str(e), fg="red")

# Create main window
root = tk.Tk()
root.title("YouTube Video Downloader")
root.geometry("800x650")

# Create Tab Control
tab_control = ttk.Notebook(root)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab3 = ttk.Frame(tab_control)
tab_control.add(tab1, text='Search YouTube')
tab_control.add(tab2, text='Download from URL')
tab_control.add(tab3, text='Downloaded Videos')
tab_control.pack(expand=1, fill="both")

# Search YouTube tab
search_label = tk.Label(tab1, text="Search YouTube:", font=("Arial", 12))
search_label.pack(pady=(20,5))
search_entry = tk.Entry(tab1, width=50, font=("Arial", 12))
search_entry.pack()
search_button = tk.Button(tab1, text="Search", command=search_youtube, font=("Arial", 12))
search_button.pack()
search_results_label = tk.Label(tab1, text="Search Results:", font=("Arial", 12))
search_results_label.pack(pady=(20,5))
search_results = tk.Listbox(tab1, height=20, width=70, font=("Arial", 12))
search_results.pack(pady=10)
select_download_button = tk.Button(tab1, text="Select for Download", command=select_video_to_download, font=("Arial", 12))
select_download_button.pack(pady=5)
status_label = tk.Label(tab1, text="", font=("Arial", 12))
status_label.pack(pady=10)

# Download from URL tab
url_label = tk.Label(tab2, text="Enter YouTube URL:", font=("Arial", 12))
url_label.pack(pady=(20,5))
url_entry = tk.Entry(tab2, width=50, font=("Arial", 12))
url_entry.pack()
download_button = tk.Button(tab2, text="Download", command=download_from_url, font=("Arial", 12))
download_button.pack(pady=5)
status_label_url = tk.Label(tab2, text="", font=("Arial", 12))
status_label_url.pack(pady=10)

# Downloaded Videos tab
downloaded_videos_label = tk.Label(tab3, text="Downloaded Videos:", font=("Arial", 12))
downloaded_videos_label.pack(pady=(20,5))
downloaded_videos_listbox = tk.Listbox(tab3, height=5, width=70, font=("Arial", 12))
downloaded_videos_listbox.pack(pady=5)
download_path_label = tk.Label(tab3, text="", font=("Arial", 12))
download_path_label.pack()
download_path_button = tk.Button(tab3, text="Change Download Path", command=browse_directory, font=("Arial", 12))
download_path_button.pack(pady=5)
play_button = tk.Button(tab3, text="Play", command=play_video, font=("Arial", 12))
play_button.pack(pady=5)


# Set default download path
download_path = os.getcwd()
download_path_label.config(text=f"Download Path: {download_path}")
update_downloaded_videos_list()

root.mainloop()
