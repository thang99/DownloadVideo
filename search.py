import requests
import tkinter as tk
from PIL import Image, ImageTk

api_key = "AIzaSyAaNFrAdAI36Y0nTCtrRaeJr5nLus-Gx08"

def search_youtube_videos(query, api_key, max_results=5):
    base_url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "maxResults": max_results,
        "key": api_key
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    videos = []
    for item in data["items"]:
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        channel = item["snippet"]["channelTitle"]
        thumbnail = item["snippet"]["thumbnails"]["default"]["url"]
        videos.append({"title": title, "channel": channel, "thumbnail": thumbnail, "video_id": video_id})

    return videos

def show_results():
    query = entry.get()
    videos = search_youtube_videos(query, api_key)

    # Xóa kết quả cũ nếu có
    for widget in result_frame.winfo_children():
        widget.destroy()

    # Hiển thị kết quả mới
    for video in videos:
        title_label = tk.Label(result_frame, text="Tiêu đề: " + video["title"])
        title_label.pack()

        channel_label = tk.Label(result_frame, text="Kênh: " + video["channel"])
        channel_label.pack()

        image = Image.open(requests.get(video["thumbnail"], stream=True).raw)
        thumbnail = ImageTk.PhotoImage(image)
        thumbnail_label = tk.Label(result_frame, image=thumbnail)
        thumbnail_label.image = thumbnail
        thumbnail_label.pack()

        video_id_label = tk.Label(result_frame, text="Video ID: " + video["video_id"])
        video_id_label.pack()

        separator = tk.Label(result_frame, text="-------------------------------------------------")
        separator.pack()

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Tìm kiếm video trên YouTube")

# Thêm hộp nhập từ khóa tìm kiếm
entry = tk.Entry(root, width=50)
entry.pack(pady=10)

# Thêm nút tìm kiếm
search_button = tk.Button(root, text="Tìm kiếm", command=show_results)
search_button.pack()

# Tạo khung để hiển thị kết quả
result_frame = tk.Frame(root)
result_frame.pack(pady=10)

# Chạy ứng dụng
root.mainloop()
