# ----------------------------
# TikTok Video Generator with optional script
# ----------------------------
@app.route("/generate_video", methods=["GET", "POST"])
def generate_video_page():
    if "user" not in session:
        return redirect(url_for("login"))

    video_file = None
    if request.method == "POST":
        urls_input = request.form.get("urls")
        script_text = request.form.get("script")  # new: optional voiceover script

        # Split URLs by comma
        urls = [u.strip() for u in urls_input.split(",") if u.strip()]

        if not urls:
            return render_template("generate_video.html", error="❌ Please enter at least one URL.")

        # Pass both URLs and optional script to your video generator
        video_path = generate_video_from_urls(urls, script_text=script_text)
        video_file = os.path.basename(video_path)

    return render_template("generate_video.html", video_file=video_file)
