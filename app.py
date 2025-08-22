from flask import Flask, request, render_template, session, redirect, url_for, send_from_directory
import os
from video_creator_dynamic import generate_video_from_urls  # your video generator
import openai  # for AI-generated scripts

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
# Helper: Generate AI script
# ----------------------------
def generate_ai_script(product_title, product_description, style="TikTok promotional"):
    prompt = f"""
    Write a short, catchy, TikTok-style promotional script for this product:
    Title: {product_title}
    Description: {product_description}
    The script should be engaging, persuasive, and around 30-45 seconds spoken length.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )
    return response.choices[0].message.content.strip()

# ----------------------------
# TikTok Video Generator with optional script
# ----------------------------
@app.route("/generate_video", methods=["GET", "POST"])
def generate_video_page():
    if "user" not in session:
        return redirect(url_for("login"))

    video_file = None
    error = None

    if request.method == "POST":
        urls_input = request.form.get("urls")
        user_script = request.form.get("script")  # optional voiceover text

        urls = [u.strip() for u in urls_input.split(",") if u.strip()]
        if not urls:
            error = "❌ Please enter at least one URL."
        else:
            try:
                # If user did not provide a script, generate one automatically
                if not user_script:
                    # Here you could fetch product info from the first URL
                    # Example placeholder
                    product_title = "Example Product"
                    product_description = "This is an amazing product with great features."
                    user_script = generate_ai_script(product_title, product_description)

                # Generate video
                video_path = generate_video_from_urls(urls, script_text=user_script)
                video_file = os.path.basename(video_path)
            except Exception as e:
                error = f"❌ Video generation failed: {str(e)}"

    return render_template("generate_video.html", video_file=video_file, error=error)

# ----------------------------
# Download generated video
# ----------------------------
@app.route("/download/<filename>")
def download_video(filename):
    return send_from_directory("static/output", filename, as_attachment=True)

# ----------------------------
# Run Flask App
# ----------------------------
if __name__ == '__main__':
    os.makedirs("static/output", exist_ok=True)
    app.run(host='0.0.0.0', port=3000, debug=True)
