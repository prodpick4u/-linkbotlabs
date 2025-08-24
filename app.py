import os
from flask import Flask, request, render_template, session, redirect, url_for, send_from_directory, jsonify
from bs4 import BeautifulSoup
import requests
from video_creator_dynamic import generate_video_from_urls

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
@app.route("/generate_video", methods=["GET", "POST"])
def generate_video_page():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    if request.method == "GET":
        return "Send a POST request with JSON {urls: [], script: 'text'}"

    data = request.get_json()
    urls = data.get("urls", [])
    script_text = data.get("script", "")

    if not urls or not script_text:
        return jsonify({"error": "Missing URLs or script"}), 400

    try:
        image_urls = []
        for url in urls:
            if url.startswith("http"):
                if url.endswith((".jpg", ".jpeg", ".png", ".webp")):
                    # Already an image (DALL·E)
                    image_urls.append(url)
                else:
                    # Product page: extract first image
                    img_url = extract_image_url(url)
                    if img_url:
                        image_urls.append(img_url)

        if not image_urls:
            return jsonify({"error": "No images could be extracted from URLs"}), 400

        video_path = generate_video_from_urls(image_urls, script_text=script_text)
        video_file = os.path.basename(video_path)
        return jsonify({"video_file": video_file})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ----------------------------
# Generate text/script page
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
                # Placeholder: replace with GPT or PUTER API call
                output_text = f"Generated script for {product_url}"
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
