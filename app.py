import os
import time
import json
from flask import Flask, request, Response, jsonify, send_from_directory, render_template

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET", "supersecretkey")
TMP_DIR = "/tmp"
os.makedirs(TMP_DIR, exist_ok=True)

# ----------------------------
# SSE Helper: Stream Progress
# ----------------------------
def simulate_step(step_name, duration=2):
    """Simulate step progress (replace with actual processing in production)"""
    for i in range(0, 101, 10):
        yield f"data: {json.dumps({'step': step_name, 'progress': i})}\n\n"
        time.sleep(duration / 10)

# ----------------------------
# SSE Route: Generate Video with Progress
# ----------------------------
@app.route('/generate_video_stream', methods=['POST'])
def generate_video_stream():
    data = request.get_json()
    urls = data.get("urls", [])
    dalle_prompts = data.get("dalle_prompts", [])
    script_text = data.get("script", "")

    def generate():
        # Step 1: Fetch URLs
        for url in urls:
            yield from simulate_step(f"Fetching {url}", 1)

        # Step 2: Generate DALL·E images
        for prompt in dalle_prompts:
            yield from simulate_step(f"Generating DALL·E image: {prompt}", 2)

        # Step 3: Generate script / TTS
        yield from simulate_step("Generating script / narration", 1)
        yield from simulate_step("Generating TTS voiceover", 2)

        # Step 4: Video processing
        yield from simulate_step("Rendering video", 3)

        # Done: send final video file
        video_file = "demo_video.mp4"  # Replace with your generated video path
        yield f"data: {json.dumps({'step': 'Complete', 'progress': 100, 'video_file': video_file})}\n\n"

    return Response(generate(), mimetype='text/event-stream')

# ----------------------------
# Frontend Route
# ----------------------------
@app.route("/")
def home():
    return render_template("dashboard.html")

# ----------------------------
# Download Video
# ----------------------------
@app.route("/download/<filename>")
def download_video(filename):
    return send_from_directory(TMP_DIR, filename, as_attachment=True)

# ----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port, debug=True)
