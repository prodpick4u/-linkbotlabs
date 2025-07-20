
import os
import json
import google.auth
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def upload_video(video_path, title, description):
    creds_path = "client_secret.json"
    with open(creds_path, "w") as f:
        f.write(os.environ["YT_CLIENT_SECRET_JSON"])

    flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
    creds = flow.run_console()

    youtube = build("youtube", "v3", credentials=creds)
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": ["affiliate", "review"],
            "categoryId": "28"
        },
        "status": {
            "privacyStatus": "public"
        }
    }

    media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype="video/*")
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    response = request.execute()
    print("Uploaded to YouTube:", response.get("id"))
