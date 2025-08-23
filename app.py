from flask import Flask, request, render_template, session, redirect, url_for, send_from_directory
import os
import requests
from bs4 import BeautifulSoup
from video_creator_dynamic import generate_video_from_urls  # your FFmpeg-based video generator

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
# OpenAI Setup (optional)
# ----------------------------
USE_OPENAI = False
try:
    import openai
    if os.getenv("OPENAI_API_KEY"):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        USE_OPENAI = True
except ImportError:
    pass  # No OpenAI installed, fallback to template


# ----------------------------
# Script Generator
# ----------------------------
def generate_script(product_url, max_chars=1600):
    """
    Generates a TikTok-style product narration script.
    Uses OpenAI if available, otherwise falls back to a template generator.
    """
    if USE_OPENAI:
        try:
            prompt = (
                f"Write an engaging TikTok-style narration for the product page: {product_url}. "
                f"Highlight benefits, visuals, and call-to-action. Max {max_chars} characters."
            )
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                max_tokens=600  # ~1600 characters
            )
            text = response.choices[0].text.strip()
            return text[:max_chars]
        except Exception as e:
            print(f"⚠️ OpenAI failed, falling back to template: {e}")

    # --- Template fallback (no AI required) ---
    return (
        f"Discover this amazing product we found online: {product_url}! "
        f"It’s designed to make your life easier, more fun, and totally stress-free. "
        f"Imagine unboxing it, feeling the sleek design, and instantly realizing how useful it is. "
        f"From the very first use, you’ll see why so many people are talking about it. "
        f"It saves time, delivers outstanding results, and fits perfectly into your daily routine. "
        f"Whether you’re at home, at work, or on the go, this product is built to impress. "
        f"Don’t just take our word for it—thousands of happy customers have already made the switch. "
        f"Picture showing this off to friends, family, or even on TikTok—it’s a real conversation starter! "
        f"And the best part? It’s affordable, durable, and packed with features you’ll love. "
        f"Click the link, check it out, and grab yours today before it sells out. "
        f"Trust us, you won’t want to miss this! "
        f"#trending #musthave #lifestyle #shopping #tiktokfinds"
    )[:max_chars]


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
        # Try to find OpenGraph image
        og_img = soup.find("meta", property="og:image")
        if og_img and og_img.get("content"):
            return og_img["content"]
        # Fallback: first <img> tag
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


@app.route("/generate_video", methods=["GET", "POST"])
def generate_video_page():
    if "user" not in session:
        return redirect(url_for("login"))

    video_file = None
    error = None
    if request.method == "POST":
        urls_input = request.form.get("urls")
        script_text = request.form.get("script")  # optional voiceover
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

                # Generate video
                video_path = generate_video_from_urls(image_urls, script_text=script_text)
                video_file = os.path.basename(video_path)
            except Exception as e:
                error = f"❌ Video generation failed: {str(e)}"

    return render_template("generate_video.html", video_file=video_file, error=error)


@app.route("/download/<filename>")
def download_video(filename):
    return send_from_directory("/tmp", filename, as_attachment=True)


# ----------------------------
# Run Flask App
# ----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
