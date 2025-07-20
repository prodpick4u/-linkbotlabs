import os
import requests

api_key = os.getenv("YOUTUBE_API_KEY")
channel_id = "UCy-zO_2DYOrWUlI0sYJR2ZQ"

if not api_key:
    print("API key missing")
    exit(1)

url = f"https://www.googleapis.com/youtube/v3/search?key={api_key}&channelId={channel_id}&part=snippet,id&order=date&maxResults=1"

response = requests.get(url)
data = response.json()

if "items" in data and len(data["items"]) > 0:
    print("✅ YouTube API working.")
    print("Latest video title:", data["items"][0]["snippet"]["title"])
else:
    print("❌ YouTube API call failed.")
    print(data)
    exit(1)
