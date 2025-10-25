import streamlit as st
from yt_dlp import YoutubeDL
import os, datetime

st.set_page_config(page_title="YouTube Saver by هندسة", page_icon="🎬", layout="centered")
st.title("🎬 YouTube Saver by هندسة")
st.caption("Download videos or audio from YouTube (powered by yt-dlp)")

url = st.text_input("YouTube video URL")
quality = st.selectbox("Choose quality / mode", ["best", "1080p", "720p", "480p", "360p", "audio only (mp3)"])

# downloads folder inside the project
SAVE_DIR = os.path.join(os.getcwd(), "downloads")
os.makedirs(SAVE_DIR, exist_ok=True)

st.markdown("---")
status = st.empty()
progress_placeholder = st.empty()

def make_output_template():
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(SAVE_DIR, "%(title)s_" + ts + ".%(ext)s")

def progress_hook(d):
    if d.get('status') == 'downloading':
        p = d.get('_percent_str', '0.0%')
        progress_placeholder.text(f"Downloading... {p}  \n{d.get('filename','')}")
    elif d.get('status') == 'finished':
        progress_placeholder.text("Merging / finalizing...")

if st.button("Start download"):
    if not url or not url.strip():
        st.warning("Please enter a valid YouTube URL.")
    else:
        outtmpl = make_output_template()
        if quality == "audio only (mp3)":
            ydl_opts = {
                "outtmpl": outtmpl,
                "format": "bestaudio/best",
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }],
                "progress_hooks": [progress_hook],
                "quiet": True,
                "no_warnings": True,
            }
        else:
            # handle numeric qualities like 1080p -> 1080
            if quality == "best":
                fmt = "bestvideo+bestaudio/best"
            else:
                res = quality.replace("p","")
                fmt = f"bestvideo[height<={res}]+bestaudio/best/best"
            ydl_opts = {
                "outtmpl": outtmpl,
                "format": fmt,
                "merge_output_format": "mp4",
                "progress_hooks": [progress_hook],
                "quiet": True,
                "no_warnings": True,
            }

        status.info("Starting download...")
        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                abspath = os.path.abspath(filename)
                status.success("Download finished!")
                st.write(f"Saved to: `{abspath}`")
                # offer download button
                with open(abspath, "rb") as f:
                    st.download_button("Download file", f, file_name=os.path.basename(abspath))
                # show basic metadata
                st.subheader("Video info")
                st.write(f"Title: {info.get('title','-')}")
                st.write(f"Uploader: {info.get('uploader','-')}")
                dur = info.get('duration')
                if dur:
                    st.write("Duration:", str(datetime.timedelta(seconds=int(dur))))
                st.write("Views:", info.get('view_count','-'))
        except Exception as e:
            status.error(f"Error: {e}")