import os
import json
from flask import Flask, request, send_from_directory, jsonify, render_template
from io import BytesIO
from PIL import Image
import requests
import subprocess

app = Flask(__name__)
TMP_DIR = "/tmp"
os.makedirs(TMP_DIR, exist_ok=True)

# ----------------------------
# Download image from URL
# ----------------------------
def download_image(url, filename):
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
        raise RuntimeError(f"Failed to download image {url}: {e}")

# ----------------------------
# Generate video using FFmpeg
# ----------------------------
def generate_video(image_files, script_text="", voice_file=None, output_filename="output.mp4"):
    # Create FFmpeg input list
    list_file = os.path.join(TMP_DIR, "images.txt")
    with open(list_file, "w") as f:
        for img in image_files:
            f.write(f"file '{img}'\n")
            f.write("duration 3\n")
        if image_files:
            f.write(f"file '{image_files[-1]}'\n")

    video_path = os.path.join(TMP_DIR, output_filename)
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", list_file,
        "-vf", "scale=1080:-2:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,format=yuv420p",
        "-pix_fmt", "yuv420p", video_path
    ], check=True)

    # Add subtitles
    if script_text:
        srt_file = os.path.join(TMP_DIR, "subtitles.srt")
        with open(srt_file, "w") as srt:
            srt.write("1\n00:00:00,000 --> 00:00:10,000\n")
            srt.write(script_text + "\n")
        subtitled = os.path.join(TMP_DIR, f"subtitled_{output_filename}")
        subprocess.run([
            "ffmpeg", "-y", "-i", video_path, "-vf", f"subtitles={srt_file}", subtitled
        ], check=True)
        video_path = subtitled

    # Merge TTS voiceover
    if voice_file:
        voice_path = os.path.join(TMP_DIR, "voice.mp3")
        voice_file.save(voice_path)
        final_video = os.path.join(TMP_DIR, f"final_{output_filename}")
        subprocess.run([
            "ffmpeg", "-y", "-i", video_path, "-i", voice_path,
            "-c:v", "copy", "-c:a", "aac", "-shortest", final_video
        ], check=True)
        video_path = final_video

    return video_path

# ----------------------------
# Generate video endpoint
# ----------------------------
@app.route("/generate_video", methods=["POST"])
def generate_video_endpoint():
    try:
        urls = json.loads(request.form.get("urls", "[]"))
        script_text = request.form.get("script", "")
        voice_file = request.files.get("voiceover")
        dalle_urls = json.loads(request.form.get("dalle_urls", "[]"))

        image_files = []

        # Download product URLs
        for idx, url in enumerate(urls):
            try:
                img_path = download_image(url, f"url_{idx}.jpg")
                image_files.append(img_path)
            except Exception as e:
                print(f"Warning: failed to download {url} - {e}")

        # Download DALL·E images
        for idx, dalle_url in enumerate(dalle_urls):
            try:
                img_path = download_image(dalle_url, f"dalle_{idx}.jpg")
                image_files.append(img_path)
            except Exception as e:
                print(f"Warning: failed to download DALL·E image {dalle_url} - {e}")

        if not image_files:
            return jsonify({"error": "No valid images to generate video"}), 400

        video_file = generate_video(image_files, script_text, voice_file=voice_file, output_filename="final_video.mp4")
        return jsonify({"video_file": os.path.basename(video_file)})

    except Exception as e:
        print("Error generating video:", e)
        return jsonify({"error": str(e)}), 500

# ----------------------------
# Frontend dashboard
# ----------------------------
@app.route("/")
def home():
    return render_template("dashboard.html")

# ----------------------------
# Download generated video
# ----------------------------
@app.route("/download/<filename>")
def download(filename):
    return send_from_directory(TMP_DIR, filename, as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port, debug=True)
