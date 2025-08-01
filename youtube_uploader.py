import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
from googleapiclient.http import MediaFileUpload

# Set the required scope
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def upload_video(video_file, title, description):
    # Step 1: Authorize with Google
    print("🔐 Authorizing...")
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        "client_secret.json", SCOPES
    )
    credentials = flow.run_console()

    # Step 2: Build the YouTube service
    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

    # Step 3: Prepare video metadata
    request_body = {
        "snippet": {
            "categoryId": "22",
            "title": title,
            "description": description,
            "tags": ["api", "upload", "python"]
        },
        "status": {
            "privacyStatus": "unlisted"  # or "private", "public"
        }
    }

    # Step 4: Upload the video file
    print("📤 Uploading video...")
    media_file = MediaFileUpload(video_file, resumable=True)
    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media_file
    )
    response = request.execute()

    # Step 5: Confirm upload
    print("✅ Upload complete! Video ID:", response["id"])

if __name__ == "__main__":
    # Change filename and title here if needed
    upload_video("test_video.mp4", "Test Upload via API", "This video was uploaded using Python.")
