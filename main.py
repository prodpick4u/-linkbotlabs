import os
import requests
import datetime
from urllib.parse import quote

# --- Configuration ---
API_KEY = os.getenv("YOUTUBE_API_KEY")  # GitHub Secret
CHANNEL_ID = "UCy-zO_2DYOrWUlI0sYJR2ZQ"
AMAZON_TAG = "mychanneld-20"  # Your affiliate tag
POSTS_DIR = "posts"

# --- Product Database (can expand later) ---
products = {
    "Samsung Galaxy Watch": "https://www.amazon.com/dp/B0C6G7XKY4?tag=mychanneld-20",
    "Ponds Face Cream": "https://www.amazon.com/dp/B000V2F7QG?tag=mychanneld-20",
    "Augustinus Bader": "https://www.amazon.com/dp/B09LYZFV2G?tag=mychanneld-20"
}

# --- Step 1: Fetch latest YouTube video title ---
def fetch_latest_video_title():
    url = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&channelId={CHANNEL_ID}&part=snippet,id&order=date&maxResults=1"
    res = requests.get(url)
    if res.status_code != 200:
        raise Exception(f"❌ YouTube API error: {res.text}")
    data = res.json()
    return data["items"][0]["snippet"]["title"]

# --- Step 2: Match product ---
def match_product(title):
    for name in products:
        if name.lower() in title.lower():
            return name, products[name]
    return "Featured Product", "https://www.amazon.com?tag=" + AMAZON_TAG

# --- Step 3: Generate markdown blog content ---
def generate_markdown(title, product_name, product_link):
    today = datetime.date.today().isoformat()
    safe_title = quote(title.replace(" ", "_"))
    filename = f"{POSTS_DIR}/{today}-{safe_title}.md"

    content = f"""---
title: "{title}"
date: {today}
tags: [YouTube, Product Review]
---

# {product_name}

Check out this awesome product featured in our latest video: **{title}**

👉 [Buy Now on Amazon]({product_link})

Watch the full video here: https://www.youtube.com/results?search_query={quote(title)}
"""

    os.makedirs(POSTS_DIR, exist_ok=True)
    with open(filename, "w") as f:
        f.write(content)

    print(f"✅ Blog post created: {filename}")
    return filename

# --- Main Execution ---
if __name__ == "__main__":
    if not API_KEY:
        print("❌ Missing YOUTUBE_API_KEY")
        exit(1)

    try:
        video_title = fetch_latest_video_title()
        product_name, product_link = match_product(video_title)
        generate_markdown(video_title, product_name, product_link)
    except Exception as e:
        print("❌ Error:", str(e))
        exit(1)
