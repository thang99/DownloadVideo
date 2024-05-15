import tkinter as tk
from pytube import YouTube

def search_videos():
    keyword = keyword_entry.get()
    keyword = keyword.replace(" ", "+")  # Replace spaces with '+' in the search query
    try:
        global search_results 
        search_results = YouTube(f"{keyword}").search()
        update_video_list(search_results)
    except Exception as e:
        video_listbox.delete(0, tk.END)
        video_listbox.insert(tk.END, "Error: " + str(e))

def update_video_list(videos):
    video_listbox.delete(0, tk.END)
    for idx, video in enumerate(videos):
        video_listbox.insert(tk.END, f"{idx+1}. {video.title}")

def select_video(event):
    selected_index = video_listbox.curselection()
    if selected_index:
        selected_video = search_results[selected_index[0]]
        download_video(selected_video)

def download_video(video):
    try:
        yt = YouTube(video.url)
        stream = yt.streams.get_highest_resolution()
        stream.download(output_path="./")
        status_label.config(text="Download completed!")
    except Exception as e:
        status_label.config(text=f"Error: {e}")

# Create main window
root = tk.Tk()
root.title("YouTube Video Search")

# Create search entry
keyword_label = tk.Label(root, text="Enter search keyword:")
keyword_label.pack(padx=10, pady=5)

keyword_entry = tk.Entry(root, width=50)
keyword_entry.pack(padx=10, pady=5)

# Create search button
search_button = tk.Button(root, text="Search", command=search_videos)
search_button.pack(padx=10, pady=5)

# Create video listbox
video_listbox = tk.Listbox(root, height=15, width=100)
video_listbox.pack(padx=10, pady=5)

# Bind select event to video listbox
video_listbox.bind('<<ListboxSelect>>', select_video)

# Create status label
status_label = tk.Label(root, text="")
status_label.pack(padx=10, pady=5)

root.mainloop()
