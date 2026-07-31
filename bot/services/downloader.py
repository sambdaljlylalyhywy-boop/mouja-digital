import yt_dlp
import os


DOWNLOAD_PATH = "downloads"


def download_media(url: str):
    os.makedirs(DOWNLOAD_PATH, exist_ok=True)

    options = {
        "outtmpl": f"{DOWNLOAD_PATH}/%(title)s.%(ext)s",
        "format": "best",
        "noplaylist": True,
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)

        filename = ydl.prepare_filename(info)

    return filename
