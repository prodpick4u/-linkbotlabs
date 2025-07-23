from amazon_scraper import fetch_amazon_top3_with_fallback
from blog_generator import generate_blog_post, write_to_blog
from tts_module import generate_tts
from youtube_uploader import upload_video

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
    amazon_search_url = "https://www.amazon.com/s?k=kitchen"
    category = "kitchen"

    print("🔍 Fetching top 3 products...")
    products = fetch_amazon_top3_with_fallback(amazon_search_url, category)

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

    video_path = "video.mp4"  # Replace with generated video path if automated

    try:
        video_url = upload_video(video_path, script)
    except Exception as e:
        print(f"❌ Video upload failed: {e}")
        video_url = None

    print("✅ Automation complete!")
    print("📝 Blog post saved.")
    if video_url:
        print(f"📺 YouTube video uploaded: {video_url}")
    else:
        print("⚠️ Video upload skipped or failed.")

if __name__ == "__main__":
    main()
