from flask import Flask, request, render_template_string, session, redirect, url_for, send_file
import os
import subprocess
import tempfile
import shutil
from datetime import datetime
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
            return "Invalid credentials", 403
    return '''
        <h2>Login</h2>
        <form method="POST">
            Email: <input type="email" name="email" required><br>
            Password: <input type="password" name="password" required><br>
            <button type="submit">Login</button>
        </form>
    '''

# ----------------------------
# Dashboard / options
# ----------------------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return '''
        <h2>Welcome! Choose an option:</h2>
        <ul>
            <li><a href="/run">Run Automation (Blog/Video Scripts)</a></li>
            <li><a href="/generate_video">Generate TikTok Video from URLs</a></li>
        </ul>
        <p><a href="/logout">Logout</a></p>
    '''

# ----------------------------
# Logout
# ----------------------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

# ----------------------------
# Original automation route
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
            return "❌ Missing one or more keys. Fill all fields.", 400

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
                return f"❌ Automation failed:<br><pre>{result.stderr}</pre>", 500

            output_preview = ""
            try:
                with open('docs/post-beauty.html', 'r', encoding='utf-8') as f:
                    output_preview = f.read()
            except:
                output_preview = "Could not load generated preview."

            return render_template_string('''
                <h2>✅ Automation Completed!</h2>
                <p>Your blog post and video scripts have been generated.</p>
                <hr>
                <h3>Sample Blog Post Preview:</h3>
                <div style="border:1px solid #ccc; padding:10px; max-height:400px; overflow:auto;">
                  {{ output_preview | safe }}
                </div>
                <p><a href="{{ url_for('dashboard') }}">Back to Dashboard</a></p>
            ''', output_preview=output_preview)

        except subprocess.TimeoutExpired:
            return "❌ Automation timed out after 5 minutes.", 500
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    return '''
        <h2>Run Automation</h2>
        <form method="POST">
            RapidAPI Key: <input type="text" name="rapidapi_key" required><br>
            Apify Token: <input type="text" name="apify_token" required><br>
            YouTube API Key: <input type="text" name="youtube_key" required><br>
            Affiliate Tag: <input type="text" name="affiliate_tag" required><br>
            <button type="submit">Run Automation</button>
        </form>
        <p><a href="/dashboard">Back to Dashboard</a></p>
    '''

# ----------------------------
# TikTok Video Generator
# ----------------------------
@app.route("/generate_video", methods=["GET", "POST"])
def generate_video_page():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        urls_input = request.form.get("urls")
        urls = [u.strip() for u in urls_input.split(",")]
        video_path = generate_video_from_urls(urls)
        return render_template_string('''
            <h2>✅ Video Generated!</h2>
            <video width="100%" controls>
                <source src="/static/output/{{ video_file }}" type="video/mp4">
            </video>
            <p><a href="/static/output/{{ video_file }}" download>Download Video</a></p>
            <p><a href="{{ url_for('generate_video_page') }}">Generate Another</a></p>
            <p><a href="{{ url_for('dashboard') }}">Back to Dashboard</a></p>
        ''', video_file=os.path.basename(video_path))

    return '''
        <h2>Paste Product URLs (comma-separated)</h2>
        <form method="POST">
            <textarea name="urls" rows="5" cols="40"></textarea><br>
            <button type="submit">Generate Video</button>
        </form>
        <p><a href="/dashboard">Back to Dashboard</a></p>
    '''

# ----------------------------
# Run Flask App
# ----------------------------
if __name__ == '__main__':
    os.makedirs("static/output", exist_ok=True)
    app.run(host='0.0.0.0', port=3000, debug=True)
