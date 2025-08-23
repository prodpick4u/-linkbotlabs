def generate_video_from_urls(image_urls, script_text=None, output_filename="output.mp4"):
    """
    Create a simple slideshow video from a list of image URLs.
    Optionally overlay a script as subtitles.
    """
    image_files = []
    for idx, url in enumerate(image_urls, start=1):
        filename = f"frame_{idx}.jpg"
        file_path = download_and_prepare_image(url, filename)
        image_files.append(file_path)

    # Create FFmpeg input list
    list_file = os.path.join(TMP_DIR, "images.txt")
    with open(list_file, "w") as f:
        for img in image_files:
            f.write(f"file '{img}'\n")
            f.write("duration 3\n")  # each image 3s
        f.write(f"file '{image_files[-1]}'\n")

    # Output video path
    video_path = os.path.join(TMP_DIR, output_filename)

    # Build FFmpeg command (slideshow, preserve aspect ratio)
    cmd = [
        "ffmpeg",
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", list_file,
        "-vf", "scale=1080:-2:force_original_aspect_ratio=decrease,"
               "pad=1080:1920:(ow-iw)/2:(oh-ih)/2,format=yuv420p",
        "-pix_fmt", "yuv420p",
        video_path
    ]
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"❌ FFmpeg failed: {e}")

    # Add subtitles if provided
    if script_text:
        wrapped = textwrap.fill(script_text, width=40)
        subtitle_file = os.path.join(TMP_DIR, "subtitles.srt")
        total_duration = len(image_urls) * 3
        with open(subtitle_file, "w") as srt:
            srt.write("1\n")
            srt.write(f"00:00:00,000 --> 00:00:{total_duration:02},000\n")
            srt.write(wrapped + "\n")

        video_with_subs = os.path.join(TMP_DIR, f"subtitled_{output_filename}")
        cmd_subs = [
            "ffmpeg",
            "-y",
            "-i", video_path,
            "-vf", f"subtitles='{subtitle_file}'",
            video_with_subs
        ]
        try:
            subprocess.run(cmd_subs, check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"❌ FFmpeg (subtitles) failed: {e}")

        return video_with_subs

    return video_path
