import os
from flask import Flask, request, render_template, jsonify, send_from_directory, session, redirect, url_for
import requests
from bs4 import BeautifulSoup
from video_creator_dynamic import generate_video_from_urls  # your AI video generator

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET", "supersecretkey")
os.makedirs("/tmp", exist_ok=True)

# ----------------------------
# Helper: Extract product description from URL
# ----------------------------
def extract_product_description(url):
    """Fetch page and try to get description text."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        
        # Try common meta description tags first
        desc = soup.find("meta", property="og:description")
        if desc and desc.get("content"):
            return desc["content"]
        desc = soup.find("meta", attrs={"name":"description"})
        if desc and desc.get("content"):
            return desc["content"]
        
        # Fallback: first <p> text
        p = soup.find("p")
        if p:
            return p.get_text(strip=True)
        
        return "Amazing product to explore!"  # fallback text

    except Exception as e:
        print(f"⚠️ Failed to extract description from {url}: {e}")
        return "Amazing product to explore!"

# ----------------------------
# Routes
# ----------------------------
@app.route("/", methods=["GET"])
def dashboard():
    return render_template("dashboard.html")

@app.route("/generate_video", methods=["POST"])
def generate_video():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Send JSON with URLs"}), 400

    urls = data.get("urls", [])
    script_text = data.get("script", "")

    if not urls:
        return jsonify({"error": "Missing URLs"}), 400

    try:
        # Generate script from URL description if no script is provided
        if not script_text:
            descriptions = [extract_product_description(url) for url in urls]
            script_text = " ".join(descriptions)
            # optional: prepend prompt
            script_text = f"Create a short, engaging TikTok-style narration for these products: {script_text}"

        # AI generates images and video automatically
        video_path = generate_video_from_urls(urls, script_text=script_text)
        return jsonify({"video_file": os.path.basename(video_path)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/download/<filename>")
def download_video(filename):
    return send_from_directory("/tmp", filename, as_attachment=True)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("dashboard"))

# ----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
