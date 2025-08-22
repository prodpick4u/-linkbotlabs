from flask import Flask, request, render_template, session, redirect, url_for, send_from_directory
import os
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
# TikTok Video Generator
# ----------------------------
@app.route("/generate_video", methods=["GET", "POST"])
def generate_video_page():
    if "user" not in session:
        return redirect(url_for("login"))

    video_file = None
    if request.method == "POST":
        urls_input = request.form.get("urls")
        urls = [u.strip() for u in urls_input.split(",")]
        video_path = generate_video_from_urls(urls)
        video_file = os.path.basename(video_path)

    return render_template("generate_video.html", video_file=video_file)

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
