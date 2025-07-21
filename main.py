import random
from amazon_scraper import get_top_3_products
from blog_generator import generate_blog_post
from youtube_script_generator import generate_script
from tts_generator import generate_tts
from youtube_uploader import upload_to_youtube

def log(message):
    print(message)

category_urls = {
    "kitchen": "https://www.amazon.com/Best-Sellers-Kitchen/zgbs/kitchen",
    "outdoors": "https://www.amazon.com/Best-Sellers/zgbs/sporting-goods",
    "beauty": "https://www.amazon.com/Best-Sellers-Beauty/zgbs/beauty"
}

category = random.choice(list(category_urls.keys()))
url = category_urls[category]
log(f"Selected category: {category}")

products = get_top_3_products(url)
log(f"✅ Retrieved {len(products)} products")

blog_content = generate_blog_post(products)
script = generate_script(products)
audio_path = generate_tts(script)
upload_to_youtube(f"Top 3 Amazon Picks - {category.title()}", audio_path, products)

log("✅ All tasks completed successfully")
