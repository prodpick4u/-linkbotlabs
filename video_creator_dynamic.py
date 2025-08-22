import os
import requests
from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip, TextClip
from io import BytesIO
from PIL import Image

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
        print(f"⚠️ Failed to download image: {e}")
        return None

def generate_video_from_urls(urls, audio_path=None, output_path="static/output/video.mp4", watermark=None):
    """
    Generate a video from image URLs and optional audio.
    - urls: list of image URLs
    - audio_path: optional audio file path
    - watermark: optional text watermark
    """
    if not urls:
        raise ValueError("No URLs provided for video creation.")

    # Download the first image
    image_path = download_image(urls[0])
    if not image_path:
        raise RuntimeError("Failed to download any image.")

    # Use provided audio or silent placeholder
    if audio_path is None:
        from moviepy.editor import ColorClip
        audio_clip = None
        duration = 5  # default 5 seconds
    else:
        audio_clip = AudioFileClip(audio_path)
        duration = audio_clip.duration

    # Create image clip
    image_clip = ImageClip(image_path).set_duration(duration)
    if audio_clip:
        image_clip = image_clip.set_audio(audio_clip)

    # Resize and background
    resolution = (1280, 720)
    image_clip = image_clip.resize(height=resolution[1])
    if image_clip.w > resolution[0]:
        image_clip = image_clip.resize(width=resolution[0])

    background = ImageClip(color=(0, 0, 0), size=resolution).set_duration(duration)
    video = CompositeVideoClip([background, image_clip.set_position("center")])

    # Add watermark if provided
    if watermark:
        watermark_clip = TextClip(
            watermark,
            fontsize=24,
            color="white",
            font="Arial-Bold",
            stroke_color="black",
            stroke_width=2,
            method="caption"
        ).set_duration(duration).set_position(("right", "bottom"))
        video = CompositeVideoClip([video, watermark_clip])

    # Write final video
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    video.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac",
        fps=24,
        threads=4,
        verbose=True,
        logger=None,
    )

    return output_path
