def upload_to_youtube(title, audio_path, products):
    print("Uploading video with title:", title[:60])

    from youtube_uploader import upload_video  # Make sure this function exists

    video_url = upload_video(
        video_path="video.mp4",
        title=title,
        description="Top 3 Amazon Picks based on trends and reviews."
    )

    print(f"✅ YouTube video uploaded: {video_url}")
