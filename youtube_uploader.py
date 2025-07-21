def upload_to_youtube(title, audio_path, products):
    print("Uploading video with title:", title[:60])
    from youtube_uploader import upload_video  # if it returns URL
video_url = upload_video("video.mp4", "youtube_script.txt")  # Adjust if needed
log(f"✅ YouTube video uploaded: {video_url}")
