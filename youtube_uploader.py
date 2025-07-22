import os
import json
import google.auth
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def upload_video(video_path, description, title="Top Amazon Picks", category_id="22", privacy="public"):
    creds_path = "client_secret.json"
    
    flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
    creds = flow.run_console()

    youtube = build("youtube", "v3", credentials=creds)

    request_body = {
        "snippet": {
            "title": title,
            "description": description,
            "categoryId": category_id
        },
        "status": {
            "privacyStatus": privacy
        }
    }

    media = MediaFileUpload(video_path)

    upload_request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media
    )
    response = upload_request.execute()
    return f"https://youtube.com/watch?v={response['id']}"
    if __name__ == "__main__":
    video_url = upload_video(
        video_path="your_video.mp4",  # change this to your video file
        title="Automated Test Upload",
        description="Uploaded using YouTube API and Python"
    )
    print("✅ Uploaded! Video URL:", video_url)

