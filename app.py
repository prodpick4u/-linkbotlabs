import os
from flask import Flask, request, render_template, jsonify, send_from_directory, session, redirect, url_for
from bs4 import BeautifulSoup
import requests
from video_creator_dynamic import generate_video_from_urls  # your TTS + video logic

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET", "supersecretkey")
os.makedirs("/tmp", exist_ok=True)

# ----------------------------
# Helper: Extract all images from a product page
# ----------------------------
def extract_image_urls(url):
    images = []
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        # Open Graph / Twitter images
        og_img = soup.find("meta", property="og:image")
        if og_img and og_img.get("content"):
            images.append(og_img["content"])
        twitter_img = soup.find("meta", attrs={"name": "twitter:image"})
        if twitter_img and twitter_img.get("content"):
            images.append(twitter_img["content"])

        # Fallback: all <img> tags
        for img in soup.find_all("img"):
            src = img.get("src")
            if src and src not in images:
                images.append(src)

    except Exception as e:
        print(f"⚠️ Failed to extract images from {url}: {e}")
    return images

# ----------------------------
# Routes
# ----------------------------
@app.route("/", methods=["GET"])
def dashboard():
    return render_template("dashboard.html")  # your all-in-one frontend

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
                    image_urls.append(url)  # already an image
                else:
                    extracted = extract_image_urls(url)
                    if extracted:
                        image_urls.extend(extracted)

        # Remove duplicates
        image_urls = list(dict.fromkeys(image_urls))

        if not image_urls:
            return jsonify({"error": "No images could be extracted"}), 400

        # Auto-generate script if empty
        if not script_text:
            urls_summary = ", ".join(urls)
            script_text = f"Write an engaging TikTok-style narration for these products: {urls_summary}. Max 1600 characters."

        # Generate video (with optional TTS inside video_creator_dynamic)
        video_path = generate_video_from_urls(image_urls, script_text=script_text)
        return jsonify({"video_file": os.path.basename(video_path)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/download/<filename>")
def download_video(filename):
    return send_from_directory("/tmp", filename, as_attachment=True)

# ----------------------------
# Real Logout Route (clears session)
# ----------------------------
@app.route("/logout")
def logout():
    session.clear()  # clear all stored session data
    return redirect(url_for("dashboard"))  # send back to dashboard

# ----------------------------
# Main
# ----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
