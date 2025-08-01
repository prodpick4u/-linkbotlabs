import os
import json
import google_auth_oauthlib.flow
import googleapiclient.discovery
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def upload_video(video_file, title, description):
    print("🔐 Preparing OAuth credentials from environment variables...")

    YT_CLIENT_ID = os.getenv("YT_CLIENT_ID")
    YT_CLIENT_SECRET = os.getenv("YT_CLIENT_SECRET")

    if not YT_CLIENT_ID or not YT_CLIENT_SECRET:
        raise Exception("Error: YT_CLIENT_ID and YT_CLIENT_SECRET must be set in environment variables.")

    creds_dict = {
        "installed": {
            "client_id": YT_CLIENT_ID,
            "client_secret": YT_CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [
                "urn:ietf:wg:oauth:2.0:oob",
                "http://localhost"
            ]
        }
    }

    temp_filename = "temp_client_secret.json"
    with open(temp_filename, "w") as f:
        json.dump(creds_dict, f)

    try:
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            temp_filename, SCOPES
        )
        credentials = flow.run_local_server(port=0)


        youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

        request_body = {
            "snippet": {
                "categoryId": "22",
                "title": title,
                "description": description,
                "tags": ["api", "upload", "python"]
            },
            "status": {
                "privacyStatus": "unlisted"
            }
        }

        print(f"📤 Uploading video '{video_file}'...")
        media_file = MediaFileUpload(video_file, resumable=True)
        request = youtube.videos().insert(
            part="snippet,status",
            body=request_body,
            media_body=media_file
        )
        response = request.execute()

        print("✅ Upload complete! Video ID:", response["id"])

    finally:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)


if __name__ == "__main__":
    upload_video(
        "test_video.mp4",
        "Test Upload via API",
        "This video was uploaded using Python with environment variable credentials."
    )
