import yt_dlp

def get_video_url(url, quality):

    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "nocheckcertificate": True,
        "geo_bypass": True,
        "http_headers": {
            "User-Agent": "Mozilla/5.0"
        }
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    formats = info["formats"]

    video_url = None

    if quality == "audio":
        for f in formats:
            if f.get("vcodec") == "none":
                video_url = f["url"]
                break
    else:
        for f in formats:
            if f.get("height") and f["height"] <= int(quality):
                if f.get("acodec") != "none":
                    video_url = f["url"]

    return {
        "title": info["title"],
        "url": video_url
    }