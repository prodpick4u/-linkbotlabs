import os
from flask import Flask, request, render_template, jsonify, send_from_directory
from video_creator_dynamic import generate_video_from_urls
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET", "supersecretkey")
os.makedirs("/tmp", exist_ok=True)

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
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/generate_video", methods=["POST"])
def generate_video():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Send JSON with urls and optional script"}), 400

    urls = data.get("urls", [])
    script_text = data.get("script", "")

    if not urls:
        return jsonify({"error": "Missing URLs"}), 400

    try:
        image_urls = []
        for url in urls:
            if url.startswith("http"):
                if url.endswith((".jpg", ".jpeg", ".png", ".webp")):
                    image_urls.append(url)  # DALL·E or direct image
                else:
                    img_url = extract_image_url(url)
                    if img_url:
                        image_urls.append(img_url)

        if not image_urls:
            return jsonify({"error": "No images could be extracted from URLs"}), 400

        video_path = generate_video_from_urls(image_urls, script_text=script_text)
        return jsonify({"video_file": os.path.basename(video_path)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/download/<filename>")
def download_video(filename):
    return send_from_directory("/tmp", filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
