from flask import Flask, request, render_template, session, redirect, url_for, send_from_directory
import os, uuid
from video_creator_dynamic import generate_video_from_urls
from openai import OpenAI

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
# Login, Dashboard, Logout (unchanged)
# ----------------------------

@app.route("/generate_video", methods=["GET", "POST"])
def generate_video_page():
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
                # Generate AI script if user left it blank
                if not script_text:
                    prompt = (
                        f"Write a short TikTok voiceover script for these product URLs: {urls}. "
                        "Keep it fun, engaging, and suitable for a short video."
                    )
                    response = client.chat.completions.create(
                        model="gpt-5-mini",
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=150
                    )
                    script_text = response.choices[0].message.content
                    ai_generated_script = script_text

                # Ensure static/output exists
                os.makedirs("static/output", exist_ok=True)

                # Generate unique filename
                filename = f"video_{uuid.uuid4().hex}.mp4"
                output_path = os.path.join("static/output", filename)

                # Generate video
                video_path = generate_video_from_urls(
                    urls, script_text=script_text, output_path=output_path
                )
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
# Download video route
# ----------------------------
@app.route("/download/<filename>")
def download_video(filename):
    return send_from_directory("static/output", filename, as_attachment=True)
