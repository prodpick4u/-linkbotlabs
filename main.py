import os
from blog_generator import generate_blog_post
from html_generator import render_html_from_template
from your_script_module import generate_script       # Generates video script text from products
from tts_module import generate_tts                   # Generates audio file from text
from video_creator import create_video_script         # Creates video from image + audio
from youtube_uploader import upload_video             # Uploads video to YouTube
from image_downloader import download_image           # Helper to download product image

# Define your categories here
CATEGORIES = ["beauty", "health", "home-decor", "kitchen", "outdoors", "tech"]

# Set directories and template
DOCS_DIR = "docs"
TEMPLATE_DIR = "templates"
HTML_TEMPLATE = "post_template.html"  # Your post HTML template

# Ensure output directory exists
os.makedirs(DOCS_DIR, exist_ok=True)

def process_category(category):
    print(f"⚙️ Processing category: {category}")

    # Step 1: Generate blog content and get product data
    markdown_content, context = generate_blog_post(category)

    # Save markdown file
    markdown_path = os.path.join(DOCS_DIR, f"blog_post-{category}.md")
    with open(markdown_path, "w", encoding="utf-8") as md_file:
        md_file.write(markdown_content)
    print(f"📝 Saved Markdown: {markdown_path}")

    # Render HTML post using template and context
    html_output_path = os.path.join(DOCS_DIR, f"post-{category}.html")
    render_html_from_template(
        template_name=HTML_TEMPLATE,
        context=context,
        output_path=html_output_path
    )
    print(f"🌐 Saved HTML: {html_output_path}")

    # Step 2: Generate YouTube script text from product data
    products = context.get("products", [])
    if not products:
        print("⚠️ No products found for video generation.")
        return

    video_script_text = generate_script(products)

    # Step 3: Generate TTS audio from script
    audio_path = generate_tts(video_script_text)

    # Step 4: Download first product image for video background
    first_image_url = products[0].get("image_url")
    if not first_image_url:
        print("⚠️ No image URL found, skipping video generation.")
        return

    image_path = download_image(first_image_url)
    if not image_path:
        print("⚠️ Image download failed, skipping video generation.")
        return

    # Step 5: Create video from image and audio
    video_path = create_video_script(image_path, audio_path)

    # Step 6: Upload video to YouTube
    video_url = upload_video(
        video_path,
        title=f"{category.title()} Product Review & Demo",
        description=video_script_text,
        tags=[category, "affiliate", "review"]
    )

    print(f"🎥 Video uploaded: {video_url}")

if __name__ == "__main__":
    for cat in CATEGORIES:
        process_category(cat)

    print("✅ All blog posts, videos, and uploads completed. index.html was not touched.")
