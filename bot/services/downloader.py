import yt_dlp
import os


DOWNLOAD_PATH = "downloads"


def create_download_folder():
    os.makedirs(DOWNLOAD_PATH, exist_ok=True)


def download_video(url: str):
    create_download_folder()

    options = {
        "outtmpl": f"{DOWNLOAD_PATH}/%(title)s.%(ext)s",
        "format": "best",
        "noplaylist": True,
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

    return filename


def download_audio(url: str):
    create_download_folder()

    options = {
        "outtmpl": f"{DOWNLOAD_PATH}/%(title)s.%(ext)s",
        "format": "bestaudio/best",
        "noplaylist": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

    filename = os.path.splitext(filename)[0] + ".mp3"

    return filename
