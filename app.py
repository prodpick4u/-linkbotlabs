from flask import Flask, request, render_template, session, redirect, url_for, send_from_directory
import os, uuid, time
import asyncio
from video_creator_dynamic import generate_video_from_urls
from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
app.secret_key = "supersecretkey"

# ----------------------------
# Simple subscription simulation
# ----------------------------
SUBSCRIBERS = {"user@example.com": "password123"}

# ----------------------------
# OpenAI Client
# ----------------------------
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# ----------------------------
# Executor for blocking tasks
# ----------------------------
executor = ThreadPoolExecutor(max_workers=2)

# ----------------------------
# Cleanup helper
# ----------------------------
def cleanup_old_videos(folder="static/output", max_age_seconds=3600):
    now = time.time()
    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)
        if os.path.isfile(path):
            if now - os.path.getmtime(path) > max_age_seconds:
                try:
                    os.remove(path)
                    print(f"🗑️ Deleted old video: {filename}")
                except Exception as e:
                    print(f"⚠️ Could not delete {filename}: {e}")

# ----------------------------
# Async wrapper for video generation
# ----------------------------
async def generate_video_async(urls, script_text, output_path):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, generate_video_from_urls, urls, script_text, output_path)

# ----------------------------
# Generate Video Route
# ----------------------------
@app.route("/generate_video", methods=["GET", "POST"])
async def generate_video_page():
    if "user" not in session:
        return redirect(url_for("login"))

    video_file = None
    error = None
    ai_generated_script = None
    script_text = None

    if request.method == "POST":
        urls_input = request.form.get("urls")
        script_text = request.form.get("script")
        urls = [u.strip() for u in urls_input.split(",") if u.strip()]

        if not urls:
            error = "❌ Please enter at least one URL."
        else:
            try:
                os.makedirs("static/output", exist_ok=True)
                cleanup_old_videos(folder="static/output", max_age_seconds=3600)

                # Generate AI script if blank
                if not script_text:
                    prompt = f"Write a short TikTok voiceover script for these product URLs: {urls}. Keep it fun, engaging, and suitable for a short video."
                    response = await asyncio.to_thread(
                        client.chat.completions.create,
                        model="gpt-5-mini",
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=150
                    )
                    script_text = response.choices[0].message.content
                    ai_generated_script = script_text

                # Generate unique filename
                filename = f"video_{uuid.uuid4().hex}.mp4"
                output_path = os.path.join("static/output", filename)

                # Generate video asynchronously
                video_path = await generate_video_async(urls, script_text, output_path)
                video_file = os.path.basename(video_path)

            except Exception as e:
                error = f"❌ Video generation failed: {e}"

    return render_template(
        "generate_video.html",
        video_file=video_file,
        error=error,
        script_text=ai_generated_script or script_text or ""
    )

# ----------------------------
# Download route
# ----------------------------
@app.route("/download/<filename>")
def download_video(filename):
    return send_from_directory("static/output", filename, as_attachment=True)

# ----------------------------
# Run Flask App
# ----------------------------
if __name__ == '__main__':
    os.makedirs("static/output", exist_ok=True)
    cleanup_old_videos(folder="static/output", max_age_seconds=3600)
    app.run(host='0.0.0.0', port=3000, debug=True)
