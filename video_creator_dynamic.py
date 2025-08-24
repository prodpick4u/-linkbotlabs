import os
import requests
from PIL import Image
from io import BytesIO
import subprocess
import textwrap


# Temp directory
TMP_DIR = "/tmp"
os.makedirs(TMP_DIR, exist_ok=True)

# OpenAI client
client = OpenAI()

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
# Generate Voiceover (TTS)
# ----------------------------
def generate_tts(script_text, output_audio="voice.mp3"):
    """
    Generate speech from text using OpenAI TTS.
    """
    audio_path = os.path.join(TMP_DIR, output_audio)
    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="alloy",  # voices: alloy, verse, copper
        input=script_text
    ) as response:
        response.stream_to_file(audio_path)
    return audio_path

# ----------------------------
# Generate Video
# ----------------------------
def generate_video_from_urls(image_urls, script_text=None, output_filename="output.mp4"):
    """
    Create a simple slideshow video from a list of image URLs.
    Optionally overlay a script as subtitles and/or generate voiceover.
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
            f.write("duration 3\n")  # 3s per image
        f.write(f"file '{image_files[-1]}'\n")  # last frame hold

    # Step 1: Make slideshow video
    video_path = os.path.join(TMP_DIR, output_filename)
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", list_file,
        "-vf", "scale=1080:-2:force_original_aspect_ratio=decrease,"
               "pad=1080:1920:(ow-iw)/2:(oh-ih)/2,format=yuv420p",
        "-pix_fmt", "yuv420p",
        video_path
    ]
    subprocess.run(cmd, check=True)

    # Step 2: Subtitles (optional)
    if script_text:
        wrapped = textwrap.fill(script_text, width=40)
        subtitle_file = os.path.join(TMP_DIR, "subtitles.srt")
        with open(subtitle_file, "w") as srt:
            srt.write("1\n")
            srt.write("00:00:00,000 --> 00:00:10,000\n")
            srt.write(wrapped + "\n")

        video_with_subs = os.path.join(TMP_DIR, f"subtitled_{output_filename}")
        cmd_subs = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-vf", f"subtitles={subtitle_file}",
            video_with_subs
        ]
        subprocess.run(cmd_subs, check=True)
        video_path = video_with_subs

    # Step 3: Voiceover (optional)
    if script_text:
        audio_path = generate_tts(script_text)
        final_output = os.path.join(TMP_DIR, f"final_{output_filename}")
        cmd_mix = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-i", audio_path,
            "-c:v", "copy",
            "-c:a", "aac",
            "-shortest",
            final_output
        ]
        subprocess.run(cmd_mix, check=True)
        return final_output

    return video_path
