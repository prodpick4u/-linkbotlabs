from flask import Flask, request, render_template, session, redirect, url_for
import os
import subprocess
import tempfile
import shutil
from video_creator_dynamic import generate_video_from_urls  # your dynamic video generator

app = Flask(__name__)
app.secret_key = "supersecretkey"  # replace with env variable in production

# ----------------------------
# Simple subscription simulation
# ----------------------------
SUBSCRIBERS = {"user@example.com": "password123"}  # demo subscribers

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
# Run Automation Route
# ----------------------------
@app.route('/run', methods=['GET', 'POST'])
def run_demo_page():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        rapidapi_key = request.form.get('rapidapi_key')
        apify_token = request.form.get('apify_token')
        youtube_key = request.form.get('youtube_key')
        affiliate_tag = request.form.get('affiliate_tag')

        if not all([rapidapi_key, apify_token, youtube_key, affiliate_tag]):
            return render_template("run.html", error="❌ Missing one or more keys. Fill all fields.")

        temp_dir = tempfile.mkdtemp()
        try:
            env = os.environ.copy()
            env['RAPIDAPI_KEY'] = rapidapi_key
            env['APIFY_TOKEN'] = apify_token
            env['YOUTUBE_API_KEY'] = youtube_key
            env['AFFILIATE_TAG'] = affiliate_tag

            result = subprocess.run(
                ['python3', 'main.py'],
                cwd='.',
                env=env,
                capture_output=True,
                text=True,
                timeout=300
            )

            if result.returncode != 0:
                return render_template("run.html", error=f"❌ Automation failed:<br><pre>{result.stderr}</pre>")

            output_preview = ""
            try:
                with open('docs/post-beauty.html', 'r', encoding='utf-8') as f:
                    output_preview = f.read()
            except:
                output_preview = "Could not load generated preview."

            return render_template("run.html", success=True, output_preview=output_preview)

        except subprocess.TimeoutExpired:
            return render_template("run.html", error="❌ Automation timed out after 5 minutes.")
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    return render_template("run.html")


# ----------------------------
# TikTok Video Generator
# ----------------------------
@app.route("/generate_video", methods=["GET", "POST"])
def generate_video_page():
    if "user" not in session:
        return redirect(url_for("login"))

    video_file = None
    if request.method == "POST":
        urls_input = request.form.get("urls")
        urls = [u.strip() for u in urls_input.split(",")]
        video_path = generate_video_from_urls(urls)
        video_file = os.path.basename(video_path)

    return render_template("generate_video.html", video_file=video_file)


# ----------------------------
# Run Flask App
# ----------------------------
if __name__ == '__main__':
    os.makedirs("static/output", exist_ok=True)
    app.run(host='0.0.0.0', port=3000, debug=True)
