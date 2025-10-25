# YouTube Saver by هندسة

Simple Streamlit app that uses `yt-dlp` to download YouTube videos or extract audio (mp3).
Designed to be deployed on **Streamlit Cloud** and also runnable locally.

## Files
- `youtube_downloader_app.py` - main Streamlit application
- `streamlit_app.py` - Streamlit Cloud entrypoint
- `requirements.txt` - Python dependencies
- `downloads/` - local folder where downloads are saved (created automatically)

## Deploy on Streamlit Cloud
1. Push this repository to GitHub.
2. Go to https://share.streamlit.io and sign in with GitHub.
3. Click **New app**, select your repository and the branch, and set the main file to `streamlit_app.py`.
4. Deploy. Streamlit Cloud will install dependencies from `requirements.txt`.
   (ffmpeg is typically available in the Streamlit Cloud environment.)

## Run locally
```bash
pip install -r requirements.txt
streamlit run youtube_downloader_app.py
```

## Notes
- If audio/video merging fails locally, ensure `ffmpeg` is installed and accessible.
- The app saves files under the `downloads/` folder inside the project root.
