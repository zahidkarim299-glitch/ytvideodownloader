from flask import Flask, render_template, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/download", methods=["POST"])
def download():

    data = request.json
    url = data.get("url")
    quality = data.get("quality", "720")

    try:

        ydl_opts = {
            "quiet": True,
            "skip_download": True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        formats = info["formats"]

        video_url = None

        if quality == "audio":
            for f in formats:
                if f.get("acodec") != "none" and f.get("vcodec") == "none":
                    video_url = f["url"]
                    break
        else:
            for f in formats:
                if f.get("height") and int(f["height"]) <= int(quality):
                    if f.get("acodec") != "none" and f.get("vcodec") != "none":
                        video_url = f["url"]

        if not video_url:
            return jsonify({"status": "error", "message": "Quality not found"})

        title = info.get("title", "video")

        return jsonify({
            "status": "success",
            "title": title,
            "download_url": video_url
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)