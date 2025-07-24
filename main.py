from datetime import datetime
from blog_generator import generate_blog_post
from video_creator import create_video_script, render_video, upload_video
import requests
from secrets import RAPIDAPI_KEY, AMAZON_TAG  # Import your secrets here

CATEGORY = "Beauty Products"  # Change as needed

def fetch_top_amazon_products(query, num=3):
    url = "https://real-time-web-search.p.rapidapi.com/search-advanced"
    headers = {
        "x-rapidapi-host": "real-time-web-search.p.rapidapi.com",
        "x-rapidapi-key": RAPIDAPI_KEY  # Use the imported key here
    }

    params = {
        "q": f"{query} site:amazon.com",
        "num": num,
        "start": 0,
        "gl": "us",
        "hl": "en",
        "device": "desktop",
        "nfpr": "0"
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print(f"API error {response.status_code}: {response.text}")
        return []

    data = response.json()
    products = []

    for result in data.get("organic", []):
        link = result.get("link")
        if "amazon.com" in link:
            affiliate_link = link.split("?")[0] + f"?tag={AMAZON_TAG}"  # Use imported affiliate tag here
            products.append({
                "title": result.get("title"),
                "link": affiliate_link,
                "description": result.get("snippet") or ""
            })
        if len(products) == num:
            break

    return products

def main():
    print(f"🔍 Fetching top 3 products for category: {CATEGORY}")
    products = fetch_top_amazon_products(CATEGORY)

    if not products:
        print("❌ No products fetched, aborting.")
        return

    today = datetime.utcnow().strftime("%Y-%m-%d")
    post_filename = f"post-{CATEGORY.lower().replace(' ', '-')}.html"

    print("📝 Generating blog post...")
    generate_blog_post(products, CATEGORY, post_filename)

    print("🎬 Creating video script...")
    video_script = create_video_script(products, CATEGORY)

    print("📹 Rendering video...")
    video_path = render_video(video_script, CATEGORY)

    print("📤 Uploading to YouTube...")
    upload_video(video_path, CATEGORY, today)

    print("✅ Done!")

if __name__ == "__main__":
    main()
