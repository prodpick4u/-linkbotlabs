import os
import requests
from io import BytesIO
from PIL import Image
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip, TextClip, concatenate_videoclips

def download_image(url, save_dir="static/output"):
    """Download an image from a URL and return local path."""
    os.makedirs(save_dir, exist_ok=True)
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()
        ext = url.split(".")[-1].split("?")[0]
        filename = f"image_{os.urandom(4).hex()}.{ext}"
        path = os.path.join(save_dir, filename)
        with open(path, "wb") as f:
            f.write(response.content)
        return path
    except Exception as e:
        print(f"⚠️ Failed to download image {url}: {e}")
        return None

def generate_tts(script_text, save_dir="static/output"):
    """Generate a TTS audio file from the script text."""
    os.makedirs(save_dir, exist_ok=True)
    tts_path = os.path.join(save_dir, f"audio_{os.urandom(4).hex()}.mp3")
    tts = gTTS(script_text)
    tts.save(tts_path)
    return tts_path

def generate_video_from_urls(urls, script_text=None, output_path="static/output/video.mp4", resolution=(1080, 1920)):
    """
    Generate a TikTok-format video from image URLs with optional voiceover script.
    - urls: list of image URLs
    - script_text: optional text for voiceover
    - resolution: output video size (width, height)
    """
    if not urls:
        raise ValueError("No URLs provided for video creation.")

    clips = []
    audio_clip = None

    # Generate audio if script is provided
    if script_text:
        audio_path = generate_tts(script_text)
        audio_clip = AudioFileClip(audio_path)
        total_duration = audio_clip.duration
    else:
        total_duration = len(urls) * 5  # default 5 seconds per image

    # Download images and create clips
    for url in urls:
        image_path = download_image(url)
        if not image_path:
            continue

        clip_duration = total_duration / len(urls) if audio_clip else 5
        img_clip = ImageClip(image_path).set_duration(clip_duration)
        
        # Resize and maintain aspect ratio
        img_clip = img_clip.resize(height=resolution[1])
        if img_clip.w > resolution[0]:
            img_clip = img_clip.resize(width=resolution[0])

        # Add black background to fit TikTok resolution
        background = ImageClip(color=(0,0,0), size=resolution).set_duration(clip_duration)
        clip = CompositeVideoClip([background, img_clip.set_position("center")])
        clips.append(clip)

    if not clips:
        raise RuntimeError("No valid images downloaded.")

    video = concatenate_videoclips(clips, method="compose")

    if audio_clip:
        video = video.set_audio(audio_clip)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    video.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac",
        fps=24,
        threads=4,
        verbose=True,
        logger=None
    )

    return output_path
