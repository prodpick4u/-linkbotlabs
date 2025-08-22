from flask import Flask, request, render_template, session, redirect, url_for, send_from_directory
import os
from video_creator_dynamic import generate_video_from_urls  # your video generator
from openai import OpenAI

app = Flask(__name__)
app.secret_key = "supersecretkey"  # replace with env variable in production

# ----------------------------
# Simple subscription simulation
# ----------------------------
SUBSCRIBERS = {"user@example.com": "password123"}  # demo subscribers

# ----------------------------
# OpenAI Client
# ----------------------------
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# ----------------------------
# Login route
# ----------------------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        if SUBSCRIBERS.get(email) == password:
            session["user"] = email
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

# ----------------------------
# Dashboard / options
# ----------------------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", user=session["user"])

# ----------------------------
# Logout
# ----------------------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

# ----------------------------
# TikTok Video Generator with optional AI script
# ----------------------------
@app.route("/generate_video", methods=["GET", "POST"])
def generate_video_page():
    if "user" not in session:
        return redirect(url_for("login"))

    video_file = None
    error = None
    ai_generated_script = None

    if request.method == "POST":
        urls_input = request.form.get("urls")
        script_text = request.form.get("script")  # optional voiceover text

        urls = [u.strip() for u in urls_input.split(",") if u.strip()]
        if not urls:
            error = "❌ Please enter at least one URL."
        else:
            try:
                # If user did not provide a script, generate one using AI
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
                    ai_generated_script = script_text  # Show in textarea for review

                # Generate video using dynamic video creator
                video_path = generate_video_from_urls(urls, script_text=script_text)
                video_file = os.path.basename(video_path)
            except Exception as e:
                error = f"❌ Video generation failed: {str(e)}"

    return render_template(
        "generate_video.html",
        video_file=video_file,
        error=error,
        script_text=ai_generated_script or script_text or ""
    )

# ----------------------------
# Download generated video
# ----------------------------
@app.route("/download/<filename>")
def download_video(filename):
    return send_from_directory("static/output", filename, as_attachment=True)

# ----------------------------
# Run Flask App
# ----------------------------
if __name__ == '__main__':
    os.makedirs("static/output", exist_ok=True)
    app.run(host='0.0.0.0', port=3000, debug=True)
