from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip, TextClip


def create_video_script(image_path, audio_path, output_path="video.mp4"):
    """
    Combines an image and audio file into a video with optional watermark.
    Returns the output video path.
    """
    print("🎬 Creating video script...")

    # Load audio and get duration
    audio = AudioFileClip(audio_path)
    duration = audio.duration

    # Create image clip with duration and audio
    image_clip = ImageClip(image_path).set_duration(duration).set_audio(audio)

    # Resize to 720p resolution with black background
    resolution = (1280, 720)
    image_clip = image_clip.resize(height=resolution[1])
    if image_clip.w > resolution[0]:
        image_clip = image_clip.resize(width=resolution[0])

    background = ImageClip(color=(0, 0, 0), size=resolution).set_duration(duration)
    video = CompositeVideoClip([background, image_clip.set_position("center")])

    # Optional watermark
    watermark_text = "prodpick4u.com"
    watermark = TextClip(
        watermark_text,
        fontsize=24,
        color="white",
        font="Arial-Bold",
        stroke_color="black",
        stroke_width=2,
        method="caption"
    ).set_duration(duration)

    video = CompositeVideoClip([
        video,
        watermark.set_pos(("right", "bottom")).margin(right=10, bottom=10)
    ])

    # Export video
    video.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac",
        fps=24,
        threads=4,
        verbose=True,
        logger=None,
    )

    print(f"✅ Video script created at {output_path}")
    return output_path


def render_video(script_path):
    """
    In this context, rendering is already done by create_video_script.
    This function exists to match main.py import.
    """
    print("🎞️ render_video called — already rendered during script creation.")


def upload_video(video_path, title="Auto Product Review", description="", tags=[]):
    """
    Placeholder uploader. Replace with real YouTube API upload if needed.
    """
    print(f"🚀 Uploading video: {video_path}")
    print(f"Title: {title}")
    print(f"Description: {description}")
    print(f"Tags: {tags}")
    print("✅ Video upload simulated (real upload logic goes here).")
