from flask import Flask, render_template, request, jsonify
from worker import get_video_url

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

        result = get_video_url(url, quality)

        return jsonify({
            "status": "success",
            "title": result["title"],
            "download_url": result["url"]
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        })


if __name__ == "__main__":
    app.run()