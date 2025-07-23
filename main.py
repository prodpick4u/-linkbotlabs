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
        script += f"Buy now: {p['link']}\n\n"
    return script

def main():
    url = "https://www.amazon.com/Best-Sellers-Kitchen/zgbs/kitchen"
    fallback_asins = ["B08ZJTX8WZ", "B07YXL5GLM", "B07PZ4PK4R"]

    print("🔍 Fetching top 3 products...")
    products = fetch_amazon_top3_with_fallback(url, fallback_asins)

    if not products:
        print("❌ No products fetched, aborting.")
        return

    print("📝 Generating blog post...")
    blog_post = generate_blog_post(products, category="Kitchen")
    write_to_blog("Kitchen", blog_post)

    print("🎬 Generating YouTube script...")
    script = generate_youtube_script(products)
    with open("youtube_script.txt", "w", encoding="utf-8") as f:
        f.write(script)

    try:
        audio_path = generate_tts(script)
    except Exception as e:
        print(f"❌ TTS generation failed: {e}")
        audio_path = None

    video_path = "video.mp4"  # Placeholder if you're generating video separately

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
