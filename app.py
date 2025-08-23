from flask import Flask, request, render_template, session, redirect, url_for, send_from_directory
import os
import requests
from bs4 import BeautifulSoup
from video_creator_dynamic import generate_video_from_urls  # your FFmpeg+TTS video generator
from utils import extract_image_urls
from openai import OpenAI

# ----------------------------
# Flask Setup
# ----------------------------
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET", "supersecretkey")  # use env variable in production
os.makedirs("/tmp", exist_ok=True)

# ----------------------------
# Simple subscription simulation
# ----------------------------
SUBSCRIBERS = {"user@example.com": "password123"}  # demo subscribers

# ----------------------------
# OpenAI Setup
# ----------------------------
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # secure key

def generate_script(product_url, max_chars=1600):
    """
    Generates a TikTok-style product narration script from a URL.
    Uses OpenAI SDK >=1.0.0.
    """
    prompt = (
        f"Write an engaging TikTok-style narration for the product page: {product_url}. "
        f"Highlight benefits, visuals, and call-to-action. Max {max_chars} characters."
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a creative TikTok script writer."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=600
    )

    text = response.choices[0].message.content
    return text[:max_chars]

# ----------------------------
# Helper: Extract first image from product page
# ----------------------------
def extract_image_url(url):
    """
    Attempt to get the first main image from a webpage.
    """
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
        else:
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
# Generate TikTok Video
# ----------------------------
@app.route("/generate_video", methods=["GET", "POST"])
def generate_video_page():
    if "user" not in session:
        return redirect(url_for("login"))

    video_file = None
    error = None
    if request.method == "POST":
        urls_input = request.form.get("urls")
        script_text = request.form.get("script")  # optional user-supplied script
        urls = [u.strip() for u in urls_input.split(",") if u.strip()]

        if not urls:
            error = "❌ Please enter at least one URL."
        else:
            try:
                # Extract first image from each URL
                image_urls = []
                for url in urls:
                    img_url = extract_image_url(url)
                    if img_url:
                        image_urls.append(img_url)
                if not image_urls:
                    raise ValueError("No images could be extracted from the URLs provided.")

                # Generate script if not provided
                if not script_text:
                    script_text = generate_script(urls[0])

                # Generate video (with subtitles + TTS voiceover)
                video_path = generate_video_from_urls(image_urls, script_text=script_text)
                video_file = os.path.basename(video_path)

            except Exception as e:
                error = f"❌ Video generation failed: {str(e)}"

    return render_template("generate_video.html", video_file=video_file, error=error)

# ----------------------------
# Generate Text / Blog / Script
# ----------------------------
@app.route("/generate_text", methods=["GET", "POST"])
def generate_text_page():
    if "user" not in session:
        return redirect(url_for("login"))

    output_text = None
    error = None
    if request.method == "POST":
        product_url = request.form.get("product_url")
        if not product_url:
            error = "❌ Please enter a product URL."
        else:
            try:
                output_text = generate_script(product_url)
            except Exception as e:
                error = f"❌ Script generation failed: {str(e)}"

    return render_template("generate_text.html", output_text=output_text, error=error)

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
