import os
from blog_generator import generate_markdown, generate_html, save_blog_files
from youtube_uploader import upload_video as real_upload_video
from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip, TextClip

def create_video_script(image_path, audio_path, output_path="video.mp4"):
    print("🎬 Creating video script...")
    audio = AudioFileClip(audio_path)
    duration = audio.duration

    image_clip = ImageClip(image_path).set_duration(duration).set_audio(audio)

    resolution = (1280, 720)
    image_clip = image_clip.resize(height=resolution[1])
    if image_clip.w > resolution[0]:
        image_clip = image_clip.resize(width=resolution[0])

    background = ImageClip(color=(0, 0, 0), size=resolution).set_duration(duration)
    video = CompositeVideoClip([background, image_clip.set_position("center")])

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

def upload_video(video_path, title="Auto Product Review", description="", tags=[]):
    try:
        video_id = real_upload_video(video_path, title, description)
        print(f"✅ Video uploaded with ID: {video_id}")
        return video_id
    except Exception as e:
        print(f"❌ Video upload failed: {e}")
        return None

def main():
    # Example blog generation step (simplified)
    title = "Top Kitchen Picks 2025"
    slug = "kitchen"
    description = "Discover the top trending kitchen gadgets and appliances in 2025."
    
    # Normally you would fetch or have product data here, for demo just skip to video step

    # Paths for video creation - replace with your actual generated image/audio files
    image_path = "path/to/sample_image.jpg"
    audio_path = "path/to/sample_audio.mp3"

    # Create video from image + audio
    video_path = create_video_script(image_path, audio_path, output_path=f"{slug}_video.mp4")

    # Upload video to YouTube
    upload_video(video_path, title=f"{title} Video Review", description=description)

if __name__ == "__main__":
    main()
