from amazon_scraper import get_top3_products
from blog_generator import generate_blog_post
from blog_writer import write_to_blog
from tts_generator import generate_voiceover
from youtube_uploader import upload_to_youtube

def main():
    print("🚀 Starting blog automation...")

    # Step 1: Scrape top 3 Amazon products
    products = get_top3_products("kitchen")  # You can change category
    if not products:
        print("❌ No products found.")
        return

    # Step 2: Generate blog content
    blog_post, log_lines = generate_blog_post(products)
    write_to_blog(blog_post)

    # Step 3: Save logs
    with open("log.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(log_lines))
    print("✅ log.txt written")

    # Step 4: Create video and upload to YouTube
    video_path = generate_voiceover(blog_post)
    upload_to_youtube(video_path)

    print("🎉 Blog + YouTube automation complete.")

if __name__ == "__main__":
    main()
