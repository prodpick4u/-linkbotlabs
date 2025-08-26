from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip, TextClip

def create_video_with_audio(
    image_path,
    audio_path,
    output_path="video.mp4",
    resolution=(1280, 720),
    watermark_text=None,
    watermark_pos=("right", "bottom"),
    watermark_margin=10,
):
    # Load audio and get duration
    audio = AudioFileClip(audio_path)
    duration = audio.duration

    # Create an image clip with the audio duration
    image_clip = ImageClip(image_path).set_duration(duration).set_audio(audio)

    # Resize image to fit into resolution, keep aspect ratio and add black bars
    image_clip = image_clip.resize(height=resolution[1])  # Resize height first
    if image_clip.w > resolution[0]:
        image_clip = image_clip.resize(width=resolution[0])  # Resize width if still too wide

    # Create a black background clip with desired resolution
    background = ImageClip(color=(0, 0, 0), size=resolution).set_duration(duration)

    # Composite the image clip over black background centered
    video = CompositeVideoClip([background, image_clip.set_position("center")])

    # Add watermark text if specified
    if watermark_text:
        watermark = TextClip(
            watermark_text,
            fontsize=24,
            color="white",
            font="Arial-Bold",
            stroke_color="black",
            stroke_width=2,
            method="caption"
        ).set_duration(duration)

        # Position watermark with margin
        pos_x = watermark_pos[0]
        pos_y = watermark_pos[1]
        video = CompositeVideoClip([video, watermark.set_pos((pos_x, pos_y), relative=True).margin(right=watermark_margin, bottom=watermark_margin)])

    # Write video file
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
