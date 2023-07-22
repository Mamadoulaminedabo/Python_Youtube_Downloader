import tkinter as tk
import os
from tkinter import ttk
from pytube import YouTube

def progress_function(stream, chunk, bytes_remaining):
    # Get the percentage of the file that has been downloaded.
    percent = (100*(file_size-bytes_remaining))/file_size
    progress_bar['value'] = percent
    root.update_idletasks()

def download_video():
    global file_size
    video_url = entry_url.get()
    try:
        yt = YouTube(video_url, on_progress_callback=progress_function)
        title = yt.title  # Get the title of the video
        stream_720p = yt.streams.filter(res="720p", progressive=True).first()
        stream_360p = yt.streams.filter(res="360p", progressive=True).first()

        # Set the YouTube cookie to handle age-restricted videos
        # yt.streams.cookie_manager.set_cookie("CONSENT=YES+cb.20210328-17-p0.en+FX+207")

        if stream_720p:
            download_path = os.path.join(os.path.expanduser("~"), "Movies", f"{title}720p.mp4")
            file_size = stream_720p.filesize
            stream_720p.download(output_path=download_path)
            label_status.config(text="720p download completed.")
        elif stream_360p:
            download_path = os.path.join(os.path.expanduser("~"), "Movies", f"{title}_360p.mp4")
            file_size = stream_360p.filesize
            stream_360p.download(output_path=download_path)
            label_status.config(text="360p download completed.")
        else:
            label_status.config(text="Error: No suitable resolution found.")
    except Exception as e:
        label_status.config(text=f"Error: {str(e)}")

# Create the main window
root = tk.Tk()
root.title("YouTube Downloader")
root.geometry("400x200")

# Create and place the widgets
label_url = tk.Label(root, text="Enter YouTube URL:")
label_url.pack(pady=10)

entry_url = tk.Entry(root, width=40)
entry_url.pack(pady=5)

button_download = tk.Button(root, text="Download", command=download_video)
button_download.pack(pady=10)

label_status = tk.Label(root, text="", fg="green")
label_status.pack()

# Create a progress bar
progress_bar = ttk.Progressbar(root, length=200, mode='determinate')
progress_bar.pack(pady=10)

# Start the GUI event loop
root.mainloop()
