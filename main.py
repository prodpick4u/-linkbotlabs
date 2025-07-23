from blog_generator import generate_blog_post, write_to_blog
from tts_module import generate_tts
from youtube_uploader import upload_video
import requests
import urllib.parse

RAPIDAPI_KEY = "1cd005eae7msh84dc8a952496e8ap11a8c8jsn1d76048c3e91"
AFFILIATE_TAG = "mychanneld-20"

def fetch_amazon_top3_with_fallback(query="best kitchen products site:amazon.com"):
    url = "https://real-time-web-search.p.rapidapi.com/search-advanced"
    params = {
        "q": query,
        "num": 10,
        "start": 0,
        "gl": "us",
        "hl": "en",
        "device": "desktop",
        "nfpr": 0
    }
    headers = {
        "x-rapidapi-host": "real-time-web-search.p.rapidapi.com",
        "x-rapidapi-key": RAPIDAPI_KEY
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        results = response.json().get("organic", [])
    except Exception as e:
        print(f"❌ Failed to fetch search results: {e}")
        return []

    products = []
    for item in results:
        url = item.get("url", "")
        title = item.get("title", "")
        if "amazon.com" in url:
            tagged_url = append_affiliate_tag(url)
            products.append({
                "title": title,
                "price": "N/A",       # You may later add price scraping if needed
                "url": tagged_url,
                "pros": "",
                "cons": ""
            })
        if len(products) >= 3:
            break

    return products

def append_affiliate_tag(url):
    parsed = urllib.parse.urlparse(url)
    query = urllib.parse.parse_qs(parsed.query)
    query["tag"] = AFFILIATE_TAG
    new_query = urllib.parse.urlencode(query, doseq=True)
    return urllib.parse.urlunparse(parsed._replace(query=new_query))

def generate_youtube_script(products):
    script = "🎬 Here are today’s top 3 Amazon picks!\n\n"
    for i, p in enumerate(products, 1):
        script += f"{i}. {p['title']} - priced at {p['price']}.\n"
        if p.get("pros"):
            script += f"Pros: {p['pros']}\n"
        if p.get("cons"):
            script += f"Cons: {p['cons']}\n"
        script += f"Buy now: {p['url']}\n\n"
    return script

def main():
    category = "kitchen"
    query = f"best {category} products site:amazon.com"

    print("🔍 Fetching top 3 products...")
    products = fetch_amazon_top3_with_fallback(query)

    if not products:
        print("❌ No products fetched, aborting.")
        return

    print("📝 Generating blog post...")
    blog_post = generate_blog_post(products, category=category)
    write_to_blog(category, blog_post)

    print("🎬 Generating YouTube script...")
    script = generate_youtube_script(products)
    with open("youtube_script.txt", "w", encoding="utf-8") as f:
        f.write(script)

    try:
        audio_path = generate_tts(script)
    except Exception as e:
        print(f"❌ TTS generation failed: {e}")
        audio_path = None

    video_path = "video.mp4"  # Replace with real video path if using generation

    try:
        video_url = upload_video(video_path, script)
    except Exception as e:
        print(f"❌ Video upload failed: {e}")
        video_url = None

    print("✅ Automation complete!")
    print("📝 Blog post saved.")
    if video_url:
        print(f"📺 YouTube video uploaded: {video_url}")

if __name__ == "__main__":
    main()
