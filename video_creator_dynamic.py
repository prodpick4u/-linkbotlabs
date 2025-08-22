# video_creator_dynamic.py
import os
from video_creator_ios import create_video_with_audio
from tts_module import generate_tts  # if you want to generate audio from text

def generate_video_from_urls(urls, output_dir="static/output"):
    """
    Simple wrapper that takes a list of URLs (or file paths for now),
    generates audio for each if needed, and creates a video using the iOS video creator.
    """
    os.makedirs(output_dir, exist_ok=True)

    videos = []

    for i, url_or_path in enumerate(urls, start=1):
        # Assume url_or_path is local image path for now
        image_path = url_or_path  # later you can extend to download from URL

        # Example: generate TTS audio for each video
        audio_text = f"This is demo audio for video {i}"  # replace with actual text input
        audio_path = os.path.join(output_dir, f"audio_{i}.mp3")
        generate_tts(audio_text, output_file=audio_path)

        video_path = os.path.join(output_dir, f"video_{i}.mp4")

        # Create video using iOS creator
        create_video_with_audio(
            image_path=image_path,
            audio_path=audio_path,
            output_path=video_path,
            resolution=(1280, 720),
            watermark_text="MyBrand",
            watermark_pos=("right", "bottom"),
            watermark_margin=10
        )

        videos.append(video_path)

    # Return the first video for simplicity
    return videos[0] if videos else None
