from amazon_scraper import get_top_3_products
from blog_generator import generate_blog_post
from youtube_script_generator import generate_script
from tts_generator import generate_tts
from youtube_uploader import upload_video

def main():
    print("🔍 Fetching top 3 products...")

    try:
        products = get_top_3_products("https://www.amazon.com/Best-Sellers-Kitchen/zgbs/kitchen")
        if not products:
            raise Exception("No products found.")
    except Exception as e:
        print(f"❌ Failed to fetch products: {e}")
        return

    print("📝 Generating blog post...")
    blog_post = generate_blog_post(products)
    with open("blog_post.txt", "w", encoding="utf-8") as f:
        f.write(blog_post)

    print("🎬 Generating video script...")
    script = generate_script(products)
    with open("youtube_script.txt", "w", encoding="utf-8") as f:
        f.write(script)

    print("🎤 Generating voiceover...")
    audio_path = generate_tts(script)

    print("📤 Uploading to YouTube...")
    try:
        video_url = upload_video("video.mp4", script)
        print("✅ Video uploaded:", video_url)
    except Exception as e:
        print(f"❌ Failed to upload video: {e}")

if __name__ == "__main__":
    main()
