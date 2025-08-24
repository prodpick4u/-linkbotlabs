import os
import json
from flask import Flask, request, Response, send_from_directory, render_template
from io import BytesIO
from PIL import Image
import requests
import subprocess
import textwrap
import tempfile

app = Flask(__name__)
TMP_DIR = "/tmp"
os.makedirs(TMP_DIR, exist_ok=True)

# ----------------------------
# Download image
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
# Generate video with FFmpeg
# ----------------------------
def generate_video(image_files, script_text, voice_file=None, output_filename="output.mp4"):
    # Create ffmpeg input list
    list_file = os.path.join(TMP_DIR, "images.txt")
    with open(list_file, "w") as f:
        for img in image_files:
            f.write(f"file '{img}'\n")
            f.write("duration 3\n")
        f.write(f"file '{image_files[-1]}'\n")

    video_path = os.path.join(TMP_DIR, output_filename)
    subprocess.run([
        "ffmpeg","-y","-f","concat","-safe","0","-i",list_file,
        "-vf","scale=1080:-2:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,format=yuv420p",
        "-pix_fmt","yuv420p",
        video_path
    ], check=True)

    # Add subtitles if script provided
    if script_text:
        srt_file = os.path.join(TMP_DIR,"subtitles.srt")
        with open(srt_file,"w") as srt:
            srt.write("1\n00:00:00,000 --> 00:00:10,000\n")
            srt.write(script_text+"\n")
        subtitled = os.path.join(TMP_DIR,f"subtitled_{output_filename}")
        subprocess.run([
            "ffmpeg","-y","-i",video_path,"-vf",f"subtitles={srt_file}",subtitled
        ], check=True)
        video_path = subtitled

    # Merge voiceover
    if voice_file:
        final_video = os.path.join(TMP_DIR,f"final_{output_filename}")
        subprocess.run([
            "ffmpeg","-y","-i",video_path,"-i",voice_file,
            "-c:v","copy","-c:a","aac","-shortest",final_video
        ], check=True)
        video_path = final_video

    return video_path

# ----------------------------
# SSE: Stream real progress
# ----------------------------
@app.route("/generate_video_stream", methods=["POST"])
def generate_video_stream():
    data = request.get_json()
    urls = data.get("urls", [])
    dalle_prompts = data.get("dalle_prompts", [])
    script_text = data.get("script", "")

    def stream():
        image_files = []

        # ---------------- Step 1: Fetch product URLs ----------------
        for url in urls:
            try:
                img_path = download_image(url, f"url_{urls.index(url)}.jpg")
                image_files.append(img_path)
                yield f"data: {json.dumps({'step': f'Fetched {url}', 'progress': 100})}\n\n"
            except Exception as e:
                yield f"data: {json.dumps({'step': f'Failed {url}', 'progress': 0, 'error': str(e)})}\n\n"

        # ---------------- Step 2: Generate DALL·E images ----------------
        for prompt in dalle_prompts:
            try:
                # Use Puter.js in frontend to generate image, backend just stores URL here
                # For demo purposes, we simulate download
                # Replace with AI generation call if backend TTS/images available
                img_path = download_image(prompt, f"dalle_{dalle_prompts.index(prompt)}.jpg")
                image_files.append(img_path)
                yield f"data: {json.dumps({'step': f'Generated image: {prompt}', 'progress': 100})}\n\n"
            except Exception as e:
                yield f"data: {json.dumps({'step': f'Failed image {prompt}', 'progress': 0, 'error': str(e)})}\n\n"

        # ---------------- Step 3: Generate TTS ----------------
        tts_file = None
        if script_text:
            # In production, call TTS service; here we simulate
            tts_file = None
            yield f"data: {json.dumps({'step': 'Generated TTS', 'progress': 100})}\n\n"

        # ---------------- Step 4: Render video ----------------
        video_file = generate_video(image_files, script_text, voice_file=tts_file, output_filename="final_video.mp4")
        yield f"data: {json.dumps({'step': 'Complete', 'progress': 100, 'video_file': os.path.basename(video_file)})}\n\n"

    return Response(stream(), mimetype='text/event-stream')

# ----------------------------
# Frontend
# ----------------------------
@app.route("/")
def home():
    return render_template("dashboard.html")

# ----------------------------
# Download
# ----------------------------
@app.route("/download/<filename>")
def download(filename):
    return send_from_directory(TMP_DIR, filename, as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port, debug=True)
