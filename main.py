from amazon_scraper import get_top_3_products
from blog_generator import generate_blog_post
from youtube_script_generator import generate_script
from tts_generator import generate_tts
from youtube_uploader import upload_to_youtube

# ✅ Use full Amazon Best Seller category URL
category_url = "https://www.amazon.com/Best-Sellers-Kitchen-Dining/zgbs/kitchen/"

try:
    print("🔍 Fetching top 3 products...")
    products = get_top_3_products(category_url)

    print("📝 Generating blog post...")
    blog_content = generate_blog_post(products)

    print("🎬 Creating YouTube script...")
    script_text = generate_script(products)

    print("🔊 Generating voiceover...")
    audio_path = generate_tts(script)

    print("📤 Uploading to YouTube...")
    upload_to_youtube("Top 3 Kitchen Picks (Best Sellers)", audio_path, products)

    print("✅ All done!")

except Exception as e:
    print(f"❌ Error: {e}")
