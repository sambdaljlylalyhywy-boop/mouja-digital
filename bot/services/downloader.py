import yt_dlp
import os


DOWNLOAD_PATH = "downloads"


def create_download_folder():
    os.makedirs(DOWNLOAD_PATH, exist_ok=True)


def download_media(url: str):
    create_download_folder()

    options = {
        "outtmpl": f"{DOWNLOAD_PATH}/%(id)s_%(autonumber)s.%(ext)s",
        "format": "best",
        "noplaylist": False,
        "ignoreerrors": True,
    }

    files = []

    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)

        if not info:
            return []

        entries = info.get("entries")

        if entries:
            for entry in entries:
                if not entry:
                    continue

                try:
                    filename = ydl.prepare_filename(entry)

                    if os.path.exists(filename):
                        files.append(filename)
                except Exception:
                    continue
        else:
            filename = ydl.prepare_filename(info)

            if os.path.exists(filename):
                files.append(filename)

    return files


def download_video(url: str):
    files = download_media(url)

    if not files:
        raise Exception("لم يتم العثور على صورة أو فيديو")

    return files[0]


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
