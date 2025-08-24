import os
from flask import Flask, request, jsonify, send_from_directory, render_template
from PIL import Image
import requests
from io import BytesIO
import subprocess
import textwrap

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET", "supersecretkey")
TMP_DIR = "/tmp"
os.makedirs(TMP_DIR, exist_ok=True)

# ----------------------------
# Helper: Download + Prepare Image
# ----------------------------
def download_and_prepare_image(url, filename):
    path = os.path.join(TMP_DIR, filename)
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        if img.mode in ("P", "RGBA"):
            img = img.convert("RGB")
        img.save(path, "JPEG")
        return path
    except Exception as e:
        raise RuntimeError(f"Failed image: {e}")

# ----------------------------
# Generate Video
# ----------------------------
def generate_video(image_urls, script_text=None, voiceover_path=None, output_filename="output.mp4"):
    image_files = [download_and_prepare_image(url, f"frame_{i}.jpg") for i, url in enumerate(image_urls, 1)]

    # FFmpeg input list
    list_file = os.path.join(TMP_DIR, "images.txt")
    with open(list_file, "w") as f:
        for img in image_files:
            f.write(f"file '{img}'\n")
            f.write("duration 3\n")
        f.write(f"file '{image_files[-1]}'\n")  # last frame hold

    video_path = os.path.join(TMP_DIR, output_filename)
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", list_file,
        "-vf", "scale=1080:-2:force_original_aspect_ratio=decrease,"
               "pad=1080:1920:(ow-iw)/2:(oh-ih)/2,format=yuv420p",
        "-pix_fmt", "yuv420p",
        video_path
    ], check=True)

    # Add subtitles
    if script_text:
        wrapped = textwrap.fill(script_text, width=40)
        subtitle_file = os.path.join(TMP_DIR, "subtitles.srt")
        with open(subtitle_file, "w") as srt:
            srt.write("1\n00:00:00,000 --> 00:00:10,000\n" + wrapped + "\n")
        subtitled_video = os.path.join(TMP_DIR, f"subtitled_{output_filename}")
        subprocess.run([
            "ffmpeg", "-y",
            "-i", video_path,
            "-vf", f"subtitles={subtitle_file}",
            subtitled_video
        ], check=True)
        video_path = subtitled_video

    # Merge voiceover if provided
    if voiceover_path:
        final_video = os.path.join(TMP_DIR, f"final_{output_filename}")
        subprocess.run([
            "ffmpeg", "-y",
            "-i", video_path,
            "-i", voiceover_path,
            "-c:v", "copy",
            "-c:a", "aac",
            "-shortest",
            final_video
        ], check=True)
        return final_video

    return video_path

# ----------------------------
# Routes
# ----------------------------
@app.route("/", methods=["GET"])
def home():
    return render_template("dashboard.html")  # Put your Puter.js HTML here in templates/

@app.route("/generate_video", methods=["POST"])
def generate_video_route():
    try:
        data = request.get_json()
        urls = data.get("urls", [])
        script_text = data.get("script", "")
        if not urls:
            return jsonify({"error": "No image URLs provided"}), 400

        video_path = generate_video(urls, script_text=script_text)
        return jsonify({"video_file": os.path.basename(video_path)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/download/<filename>")
def download_video(filename):
    return send_from_directory(TMP_DIR, filename, as_attachment=True)

# ----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))  # Render dynamic port
    app.run(host="0.0.0.0", port=port, debug=True)
