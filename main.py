from utils.amazon_scraper import get_top_products
from utils.blog_writer import generate_blog_post
from utils.tts_generator import generate_voiceover
from utils.youtube_uploader import upload_to_youtube

def main():
    products = get_top_products("electric toothbrush")
    blog = generate_blog_post(products)
    voice_path = generate_voiceover(blog)
    upload_to_youtube(blog, voice_path, products)

if __name__ == "__main__":
    main()