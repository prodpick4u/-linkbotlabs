from moviepy.editor import *

def create_video_with_audio(image_path, audio_path, output_path="video.mp4"):
    # Load background image and set duration to match audio
    audio = AudioFileClip(audio_path)
    duration = audio.duration

    image_clip = ImageClip(image_path).set_duration(duration).set_fps(24).set_audio(audio)

    # Resize to 1280x720 (YouTube standard)
    video = image_clip.resize((1280, 720))

    # Write the video
    video.write_videofile(output_path, codec="libx264", audio_codec="aac")

    return output_path
