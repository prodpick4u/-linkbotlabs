from amazon_scraper import fetch_amazon_top3_with_fallback
from blog_generator import generate_blog_post, write_to_blog
from tts_module import generate_tts
from youtube_uploader import upload_video

def main():
    url = "https://www.amazon.com/Best-Sellers-Kitchen/zgbs/kitchen"
    fallback_asins = ["B08ZJTX8WZ", "B07YXL5GLM", "B07PZ4PK4R"]

    print("🔍 Fetching top 3 products...")
    products = fetch_amazon_top3_with_fallback(url, fallback_asins)

    if not products:
        print("❌ No products fetched, aborting.")
        return

    print("📝 Generating blog post...")
    blog_post = generate_blog_post(products)
    write_to_blog(blog_post)

    print("🎬 Generating YouTube script...")
    script = generate_youtube_script(products)
    with open("youtube_script.txt", "w", encoding="utf-8") as f:
        f.write(script)

    try:
        audio_path = generate_tts(script)
    except Exception as e:
        print(f"❌ TTS generation failed: {e}")
        audio_path = None

    video_path = "video.mp4"  # TODO: Replace with actual video generation

    try:
        video_url = upload_video(video_path, script)
    except Exception as e:
        print(f"❌ Video upload failed: {e}")
        video_url = None

    print("✅ Automation complete!")
    print(f"Blog post saved.")
    if video_url:
        print(f"YouTube video URL: {video_url}")
    else:
        print("Video upload did not complete.")

if __name__ == "__main__":
    main()
