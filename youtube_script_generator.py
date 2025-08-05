from amazon_scraper import fetch_amazon_top3_with_fallback
from blog_generator import generate_blog_post, write_to_blog
from tts_module import generate_tts
from youtube_uploader import upload_video

# ✅ Define the script generator function here
def generate_script(products):
    script_lines = ["Welcome to our Top 3 Kitchen Picks! 🍽️", ""]
    for i, product in enumerate(products, 1):
        script_lines.append(f"{i}. {product['title']}")
        if 'description' in product and product['description']:
            script_lines.append(f"    - {product['description']}")
        script_lines.append(f"    - Price: {product['price']}")
        script_lines.append(f"    - Check it out here: {product['url']}")
        script_lines.append("")  # blank line between products

    script_lines.append("Like what you see? Tap the link to grab your favorite. Don’t forget to like and subscribe for more weekly picks!")
    return "\n".join(script_lines)

def main():
    # 1. Fetch products (Playwright first, fallback to API)
    url = "https://www.amazon.com/Best-Sellers-Kitchen/zgbs/kitchen"
    fallback_asins = ["B08ZJTX8WZ", "B07YXL5GLM", "B07PZ4PK4R"]

    products = fetch_amazon_top3_with_fallback(url, fallback_asins)

    if not products:
        print("No products fetched, aborting.")
        return

    # 2. Generate blog post
    blog_post = generate_blog_post(products)
    write_to_blog(blog_post)

    # 3. Generate YouTube video script (VOICEOVER TEXT)
    script_text = generate_script(products)

    # 4. Generate audio voiceover from script
    audio_path = generate_tts(script_text)

    # 5. Create or assemble video with audio (your existing video creation code)
    video_path = "video.mp4"  # your video file generation logic

    # 6. Upload video to YouTube
    video_url = upload_video(video_path, script_text)

    print("Automation complete!")
    print(f"Video URL: {video_url}")

if __name__ == "__main__":
    main()
