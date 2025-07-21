from utils.blog_generator import generate_blog_post
from utils.blog_writer import write_to_blog
from utils.amazon_scraper import get_top3_products
from utils.tts_generator import generate_voiceover
from utils.youtube_uploader import upload_to_youtube

def main():
    print("🚀 Starting blog automation...")

    # 1. Scrape Amazon top 3 products
    products = get_top3_products(category="kitchen")
    if not products:
        print("❌ No products found.")
        return

    # 2. Generate blog post
    blog_post, log_lines = generate_blog_post(products)
    write_to_blog(blog_post)

    # 3. Save log
    with open("log.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(log_lines))
    print("✅ log.txt written")

    # 4. Generate voiceover and video (optional)
    video_path = generate_voiceover(blog_post)
    upload_to_youtube(video_path)

    print("🎉 Automation complete.")

if __name__ == "__main__":
    main()
