import os
import requests
from gtts import gTTS
from moviepy.editor import (
    ImageClip, AudioFileClip, CompositeVideoClip,
    concatenate_videoclips, ColorClip
)

SAFE_TMP = "/tmp"  # always safe on Render

def download_image(url, save_dir=SAFE_TMP):
    """Download an image from a URL and return local path."""
    os.makedirs(save_dir, exist_ok=True)
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()
        ext = url.split(".")[-1].split("?")[0]
        if len(ext) > 4:  # fallback if extension looks wrong
            ext = "jpg"
        filename = f"image_{os.urandom(4).hex()}.{ext}"
        path = os.path.join(save_dir, filename)
        with open(path, "wb") as f:
            f.write(response.content)
        return path
    except Exception as e:
        print(f"⚠️ Failed to download image {url}: {e}")
        return None

def generate_tts(script_text, save_dir=SAFE_TMP):
    """Generate a TTS audio file from the script text."""
    os.makedirs(save_dir, exist_ok=True)
    tts_path = os.path.join(save_dir, f"audio_{os.urandom(4).hex()}.mp3")
    tts = gTTS(script_text[:5000])  # gTTS safe limit
    tts.save(tts_path)
    return tts_path

def generate_video_from_urls(
    urls, script_text=None,
    output_path=os.path.join(SAFE_TMP, "video.mp4"),
    resolution=(720, 1280)  # optimized for TikTok + Render free plan
):
    """
    Generate a TikTok-format video from image URLs with optional voiceover script.
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
        total_duration = len(urls) * 5  # default 5s per image

    # Download images and create clips
    for url in urls:
        image_path = download_image(url)
        if not image_path:
            continue

        clip_duration = total_duration / len(urls) if audio_clip else 5
        img_clip = ImageClip(image_path).set_duration(clip_duration)

        # Resize while maintaining ratio
        img_clip = img_clip.resize(height=resolution[1])
        if img_clip.w > resolution[0]:
            img_clip = img_clip.resize(width=resolution[0])

        # Black background to fit TikTok resolution
        background = ColorClip(size=resolution, color=(0, 0, 0)).set_duration(clip_duration)
        clip = CompositeVideoClip([background, img_clip.set_position("center")])
        clips.append(clip)

    if not clips:
        raise RuntimeError("No valid images downloaded.")

    video = concatenate_videoclips(clips, method="compose")

    if audio_clip:
        video = video.set_audio(audio_clip)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Write video with Render-friendly settings
    video.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac",
        fps=24,
        threads=1,  # low to avoid Render free-plan crash
        preset="veryfast",
        bitrate="3000k",
        temp_audiofile=os.path.join(SAFE_TMP, "temp-audio.m4a"),
        remove_temp=True,
        verbose=False,
        logger=None
    )

    return output_path
