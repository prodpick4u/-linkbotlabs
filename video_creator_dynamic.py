import os
import requests
from PIL import Image
from gtts import gTTS
import subprocess

SAFE_TMP = "/tmp"  # safe for Render, Replit, etc.

def download_image(url, save_dir=SAFE_TMP):
    os.makedirs(save_dir, exist_ok=True)
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()
        ext = url.split(".")[-1].split("?")[0]
        if len(ext) > 4: ext = "jpg"
        filename = f"image_{os.urandom(4).hex()}.{ext}"
        path = os.path.join(save_dir, filename)
        with open(path, "wb") as f:
            f.write(response.content)
        return path
    except Exception as e:
        print(f"⚠️ Failed to download image {url}: {e}")
        return None

def generate_tts(script_text, save_dir=SAFE_TMP):
    os.makedirs(save_dir, exist_ok=True)
    tts_path = os.path.join(save_dir, f"audio_{os.urandom(4).hex()}.mp3")
    tts = gTTS(script_text[:5000])  # gTTS safe limit
    tts.save(tts_path)
    return tts_path

def generate_video_from_urls(urls, script_text=None, output_path=os.path.join(SAFE_TMP, "video.mp4"), resolution=(720, 1280)):
    """
    Generate a TikTok-style video from image URLs and optional voiceover script.
    """
    if not urls:
        raise ValueError("No URLs provided for video creation.")

    # Generate TTS audio if script is provided
    if script_text:
        audio_path = generate_tts(script_text)
    else:
        audio_path = None

    # Prepare images
    image_files = []
    for url in urls:
        path = download_image(url)
        if path:
            # Resize to fit resolution
            img = Image.open(path)
            img.thumbnail(resolution, Image.LANCZOS)
            resized_path = os.path.join(SAFE_TMP, f"resized_{os.path.basename(path)}")
            img.save(resized_path)
            image_files.append(resized_path)

    if not image_files:
        raise RuntimeError("No valid images downloaded.")

    # Create a temporary file list for ffmpeg
    list_file = os.path.join(SAFE_TMP, "images.txt")
    with open(list_file, "w") as f:
        for img_file in image_files:
            f.write(f"file '{img_file}'\n")
            f.write(f"duration 5\n")  # 5 seconds per image
        f.write(f"file '{image_files[-1]}'\n")  # last image stays

    # FFmpeg command to create video
    cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", list_file,
        "-vf", f"scale={resolution[0]}:{resolution[1]}:force_original_aspect_ratio=decrease,pad={resolution[0]}:{resolution[1]}:(ow-iw)/2:(oh-ih)/2:black",
    ]

    if audio_path:
        cmd += ["-i", audio_path, "-shortest"]

    cmd += ["-c:v", "libx264", "-c:a", "aac", "-pix_fmt", "yuv420p", output_path]

    subprocess.run(cmd, check=True)
    return output_path

# ----------------------
# Example usage
# ----------------------
if __name__ == "__main__":
    urls = [
        "https://via.placeholder.com/720x1280.png?text=Slide+1",
        "https://via.placeholder.com/720x1280.png?text=Slide+2"
    ]
    video = generate_video_from_urls(urls, script_text="Hello world from TTS!")
    print("✅ Video created at:", video)
