from amazon_scraper import get_top_3_products
from blog_generator import generate_blog_post
from blog_writer import write_to_blog
from tts_generator import generate_voiceover
from youtube_uploader import upload_to_youtube
import datetime

def log_to_file(log_lines):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = f"📝 Log generated on {timestamp}\n"
    with open("log.txt", "w", encoding="utf-8") as f:
        f.write(header + "\n".join(log_lines))
    print("✅ log.txt written")

def main():
    print("🚀 Starting daily content automation...")

    # Step 1: Scrape top 3 Amazon products
    category = "kitchen"  # Change to "beauty", "outdoors", etc.
    products = get_top_3_products(category)

    if not products:
        print("❌ No products found.")
        return

    # Step 2: Generate blog content
    blog_post, log_lines = generate_blog_post(products)
    write_to_blog(blog_post)

    # Step 3: Save log
    log_to_file(log_lines)

    # Step 4: Create video from blog and upload
    video_path = generate_voiceover(blog_post)
    upload_to_youtube(video_path)

    print("🎉 All tasks completed successfully!")

if __name__ == "__main__":
    main()
