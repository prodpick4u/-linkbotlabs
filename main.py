import os
from datetime import datetime
from blog_generator import generate_blog_post, write_to_blog
from tts_generator import generate_tts
from video_creator import create_video_script, render_video
from youtube_uploader import upload_video
from your_script_module import generate_script  # your video script generator function

import requests

# Your keys here - replace with environment variables if you prefer
RAPIDAPI_KEY = "1cd005eae7msh84dc8a952496e8ap11a8c8jsn1d76048c3e91"
AMAZON_TAG = "mychanneld-20"

def fetch_best_sellers(category="beauty", country="us", page=1, limit=3):
    url = "https://realtime-amazon-data.p.rapidapi.com/best-sellers"
    headers = {
        "x-rapidapi-host": "realtime-amazon-data.p.rapidapi.com",
        "x-rapidapi-key": RAPIDAPI_KEY
    }
    params = {
        "category": category,
        "country": country,
        "page": page
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print(f"❌ API error {response.status_code}: {response.text}")
        return []

    data = response.json()
    products = data.get("products", [])

    # Add affiliate tag to links
    for product in products:
        if product.get("link"):
            product["link"] += f"?tag={AMAZON_TAG}"

    return products[:limit]

def main():
    print("🔍 Fetching top 3 best sellers in Beauty...\n")
    products = fetch_best_sellers()

    if not products:
        print("❌ No products fetched, aborting.")
        return

    # Generate blog post HTML content
    blog_post = generate_blog_post(products)

    # Save blog post to file
    post_filename = "post-beauty.html"
    write_to_blog(blog_post, post_filename)
    print(f"📝 Blog post saved to {post_filename}")

    # Generate video script text (voiceover)
    script_text = generate_script(products)

    # Generate TTS audio from script text
    audio_path = generate_tts(script_text)
    print(f"🎤 Audio generated at {audio_path}")

    # Create video (e.g., using static images and audio)
    video_script = create_video_script(products, audio_path)
    video_path = render_video(video_script)
    print(f"🎬 Video rendered at {video_path}")

    # Upload video to YouTube
    today = datetime.utcnow().strftime("%Y-%m-%d")
    video_url = upload_video(video_path, f"Top Beauty Products {today}", script_text)
    print(f"📤 Video uploaded! Watch here: {video_url}")

    print("✅ Automation complete!")

if __name__ == "__main__":
    main()
