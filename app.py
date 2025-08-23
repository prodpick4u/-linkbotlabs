from flask import Flask, request, render_template, session, redirect, url_for, send_from_directory
import os
import requests
from bs4 import BeautifulSoup
from video_creator_dynamic import generate_video_from_urls  # your FFmpeg video generator

app = Flask(__name__)
app.secret_key = "supersecretkey"  # replace with env variable in production

# ----------------------------
# Simple subscription simulation
# ----------------------------
SUBSCRIBERS = {"user@example.com": "password123"}  # demo subscribers

# ----------------------------
# Helper: extract main image from any URL
# ----------------------------
def extract_image_url(page_url):
    """
    Tries to extract the main image from any web page.
    Returns the first valid image URL or None.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
        }
        response = requests.get(page_url, headers=headers, timeout=10)
        response.raise_for_status()
        html = response.text

        soup = BeautifulSoup(html, "html.parser")

        # 1️⃣ Open Graph image
        og_image = soup.find("meta", property="og:image")
        if og_image and og_image.get("content"):
            return og_image["content"]

        # 2️⃣ Twitter card image
        twitter_image = soup.find("meta", property="twitter:image")
        if twitter_image and twitter_image.get("content"):
            return twitter_image["content"]

        # 3️⃣ Fallback: first <img>
        imgs = soup.find_all("img", src=True)
        if imgs:
            src = imgs[0]["src"]
            if src.startswith("//"):
                src = "https:" + src
            elif src.startswith("/"):
                src = page_url.rstrip("/") + src
            return src

        return None
    except Exception as e:
        print(f"⚠️ Could not extract image from {page_url}: {e}")
        return None

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
# TikTok Video Generator with automatic image extraction
# ----------------------------
@app.route("/generate_video", methods=["GET", "POST"])
def generate_video_page():
    if "user" not in session:
        return redirect(url_for("login"))

    video_file = None
    error = None
    if request.method == "POST":
        urls_input = request.form.get("urls")
        script_text = request.form.get("script")  # optional voiceover script
        urls = [u.strip() for u in urls_input.split(",") if u.strip()]

        if not urls:
            error = "❌ Please enter at least one URL."
        else:
            try:
                # Extract image URLs from each page
                image_urls = []
                for url in urls:
                    img_url = extract_image_url(url)
                    if img_url:
                        image_urls.append(img_url)

                if not image_urls:
                    raise ValueError("No images could be extracted from the URLs provided.")

                # Generate video
                video_path = generate_video_from_urls(image_urls, script_text=script_text)
                video_file = os.path.basename(video_path)
            except Exception as e:
                error = f"❌ Video generation failed: {str(e)}"

    return render_template("generate_video.html", video_file=video_file, error=error)

# ----------------------------
# Download generated video
# ----------------------------
@app.route("/download/<filename>")
def download_video(filename):
    return send_from_directory("/tmp", filename, as_attachment=True)

# ----------------------------
# Run Flask App
# ----------------------------
if __name__ == '__main__':
    os.makedirs("/tmp", exist_ok=True)
    app.run(host='0.0.0.0', port=3000, debug=True)
