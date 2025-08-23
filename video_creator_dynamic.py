import os
import requests
from PIL import Image
from io import BytesIO
import subprocess
import textwrap

TMP_DIR = "/tmp"
os.makedirs(TMP_DIR, exist_ok=True)

# ----------------------------
# Download + Prepare Image
# ----------------------------
def download_and_prepare_image(url, filename):
    """
    Download an image from a URL, convert to RGB if needed, and save as JPEG.
    """
    save_path = os.path.join(TMP_DIR, filename)
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        img = Image.open(BytesIO(response.content))

        # Convert unsupported modes
        if img.mode in ("P", "RGBA"):
            img = img.convert("RGB")

        img.save(save_path, "JPEG")
        return save_path
    except Exception as e:
        raise RuntimeError(f"❌ Failed to process image from {url}: {e}")

# ----------------------------
# Generate Video
# ----------------------------
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
        # Ensure last frame holds
        f.write(f"file '{image_files[-1]}'\n")

    # Output video path
    video_path = os.path.join(TMP_DIR, output_filename)

    # Build FFmpeg command (slideshow)
    cmd = [
        "ffmpeg",
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", list_file,
        "-vf", "scale=1080:1920,format=yuv420p",
        "-pix_fmt", "yuv420p",
        video_path
    ]
    subprocess.run(cmd, check=True)

    # Add subtitles if provided
    if script_text:
        wrapped = textwrap.fill(script_text, width=40)
        subtitle_file = os.path.join(TMP_DIR, "subtitles.srt")
        with open(subtitle_file, "w") as srt:
            srt.write("1\n")
            srt.write("00:00:00,000 --> 00:00:10,000\n")
            srt.write(wrapped + "\n")

        video_with_subs = os.path.join(TMP_DIR, f"subtitled_{output_filename}")
        cmd_subs = [
            "ffmpeg",
            "-y",
            "-i", video_path,
            "-vf", f"subtitles={subtitle_file}",
            video_with_subs
        ]
        subprocess.run(cmd_subs, check=True)
        return video_with_subs

    return video_path
