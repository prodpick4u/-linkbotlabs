from amazon_scraper import get_top_3_products
from blog_generator import generate_blog_post
from youtube_script_generator import generate_script
from tts_generator import generate_tts
from youtube_uploader import upload_video

def main():
    print("🔍 Fetching top 3 products...")
    try:
        products = get_top_3_products("https://www.amazon.com/Best-Sellers-Kitchen/zgbs/kitchen")
    except Exception as e:
        print(f"❌ Failed to fetch products: {e}")
        products = []

    if not products:
        print("❌ No products found. Exiting.")
        return

    print("📝 Generating blog post...")
    generate_blog_post(products)

    print("🎬 Generating video script...")
    script = generate_script(products)

    # Save script to a file
    with open("youtube_script.txt", "w", encoding="utf-8") as f:
        f.write(script)

    print("🎤 Generating voiceover...")
    audio_path = generate_tts(script)

    print("📤 Uploading to YouTube...")
    video_url = upload_video("video.mp4", script)  # Or replace `script` with `audio_path` if needed

    print("✅ All done! Video uploaded to:", video_url)

if __name__ == "__main__":
    main()
