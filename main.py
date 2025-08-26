import os
import sys
import random
from datetime import datetime
from blog_generator import generate_blog_post
from html_generator import render_html_from_template

# Check if running in GitHub Actions
IN_GITHUB = os.environ.get("GITHUB_ACTIONS") == "true"

# Only import video modules for local runs
if not IN_GITHUB:
    from youtube_script_generator import generate_script
    from tts_module import generate_tts
    from video_creator import create_video_script
    from youtube_uploader import upload_video
    from image_downloader import download_image

# Categories available for daily posts
CATEGORIES = ["beauty", "health", "home-decor", "kitchen", "outdoors", "tech"]

# Folders and template
DOCS_DIR = "docs"
TEMPLATE_DIR = "templates"
HTML_TEMPLATE = "post_template.html"

os.makedirs(DOCS_DIR, exist_ok=True)

def process_category(category):
    print(f"⚙️ Processing category: {category}")

    # Generate blog post content
    markdown_content, context = generate_blog_post(category)

    # Timestamp for unique filenames
    today = datetime.now().strftime("%Y-%m-%d")

    # Save Markdown (for reference)
    markdown_path = os.path.join(DOCS_DIR, f"blog_{category}_{today}.md")
    with open(markdown_path, "w", encoding="utf-8") as md_file:
        md_file.write(markdown_content)
    print(f"📝 Saved Markdown: {markdown_path}")

    # Save HTML post
    html_output_path = os.path.join(DOCS_DIR, f"post_{category}_{today}.html")
    render_html_from_template(
        template_name=HTML_TEMPLATE,
        context=context,
        output_path=html_output_path
    )
    print(f"🌐 Saved HTML: {html_output_path}")

    # Skip video creation/upload on GitHub
    if IN_GITHUB:
        print("🚫 Skipping video and YouTube steps in GitHub Actions.")
        return

    # Local video workflow
    products = context.get("products", [])
    if not products:
        print("⚠️ No products found for video generation.")
        return

    video_script_text = generate_script(products)
    audio_path = generate_tts(video_script_text)

    first_image_url = products[0].get("image_url")
    if not first_image_url:
        print("⚠️ No image URL found, skipping video generation.")
        return

    image_path = download_image(first_image_url)
    if not image_path:
        print("⚠️ Image download failed, skipping video generation.")
        return

    video_path = create_video_script(image_path, audio_path)

    video_url = upload_video(
        video_path,
        title=f"{category.title()} Product Review & Demo",
        description=video_script_text,
        tags=[category, "affiliate", "review"]
    )
    print(f"🎥 Video uploaded: {video_url}")

if __name__ == "__main__":
    # Select ONE category per day for GitHub automation
    if IN_GITHUB:
        category = random.choice(CATEGORIES)
        process_category(category)
    else:
        # Local run: process all categories
        for cat in CATEGORIES:
            process_category(cat)

    print("✅ Daily blog generation complete. Video steps skipped on GitHub.")
