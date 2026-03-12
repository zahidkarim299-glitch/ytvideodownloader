from flask import Flask, request, jsonify, render_template
import yt_dlp

app = Flask(__name__)

progress_data = {"percent": 0}

@app.route("/")
def home():
    return render_template("index.html")


def progress_hook(d):

    if d['status'] == 'downloading':
        percent = d['_percent_str'].replace('%','').strip()
        progress_data["percent"] = percent

    if d['status'] == 'finished':
        progress_data["percent"] = 100


@app.route("/download", methods=["POST"])
def download():

    data = request.json
    url = data["url"]

    ydl_opts = {
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'progress_hooks': [progress_hook]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return jsonify({"message": "Download finished"})


@app.route("/progress")
def progress():
    return jsonify(progress_data)


app.run(debug=True)