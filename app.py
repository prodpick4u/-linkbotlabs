from flask import Flask, request, render_template, session, redirect, url_for, send_from_directory, jsonify
import os
import requests
from bs4 import BeautifulSoup
from video_creator_dynamic import generate_video_from_urls  # your FFmpeg+TTS video generator

# ----------------------------
# Flask Setup
# ----------------------------
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET", "supersecretkey")
os.makedirs("/tmp", exist_ok=True)

# ----------------------------
# Simple subscription simulation
# ----------------------------
SUBSCRIBERS = {"user@example.com": "password123"}  # demo subscribers

# ----------------------------
# Helper: Extract first image from product page
# ----------------------------
def extract_image_url(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        img = soup.find("img")
        if img and img.get("src"):
            return img["src"]
    except Exception as e:
        print(f"⚠️ Failed to extract image from {url}: {e}")
    return None

# ----------------------------
# Routes
# ----------------------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        if SUBSCRIBERS.get(email) == password:
            session["user"] = email
            return redirect(url_for("dashboard"))
        return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", user=session["user"])

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

# ----------------------------
# Generate TikTok Video (JSON POST)
# ----------------------------
@app.route("/generate_video", methods=["POST"])
def generate_video_page():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    urls = data.get("urls", [])
    script_text = data.get("script", "")

    if not urls or not script_text:
        return jsonify({"error": "Missing URLs or script"}), 400

    try:
        # Extract first image from each URL
        image_urls = []
        for url in urls:
            img_url = extract_image_url(url)
            if img_url:
                image_urls.append(img_url)
        if not image_urls:
            return jsonify({"error": "No images could be extracted from URLs"}), 400

        # Generate video (FFmpeg + TTS)
        video_path = generate_video_from_urls(image_urls, script_text=script_text)
        video_file = os.path.basename(video_path)
        return jsonify({"video_file": video_file})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ----------------------------
# Download generated video
# ----------------------------
@app.route("/download/<filename>")
def download_video(filename):
    return send_from_directory("/tmp", filename, as_attachment=True)

# ----------------------------
# Run Flask App
# ----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
