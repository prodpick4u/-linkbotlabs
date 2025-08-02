import os
import json
import random
from fetch_best_sellers import fetch_best_sellers
from blog_generator import generate_markdown, save_blog_files, generate_html
from index_generator import generate_index_html
from fallback_products import get_fallback_products
from dotenv import load_dotenv

if os.path.exists(".env"):
    load_dotenv()
    print("🔧 Loaded environment from .env")

categories = [
    {"slug": "kitchen", "title": "Top Kitchen Gadgets on Amazon", "description": "Explore the best kitchen tools, appliances, and gadgets trending now."},
    {"slug": "outdoors", "title": "Outdoor Gear Must-Haves", "description": "Gear up for your next adventure with these outdoor best sellers."},
    {"slug": "beauty", "title": "Amazon Beauty Best Sellers", "description": "Discover the most loved beauty and skincare products."},
    {"slug": "home-decor", "title": "Stylish Home Decor on Amazon", "description": "Add a touch of charm to your home with these decorative finds."},
    {"slug": "tech", "title": "Best Tech Gadgets 2025", "description": "From smart devices to must-have accessories, here's what's trending in tech."},
    {"slug": "health", "title": "Health & Wellness Picks", "description": "Stay healthy and fit with these top-rated wellness products."},
]

MIN_PRODUCTS = 3
FALLBACK_SELECT_COUNT = 5  # number of fallback products to pick

for category in categories:
    slug = category["slug"]
    title = category["title"]
    description = category["description"]

    print(f"🚀 Generating blog for category: {slug}")

    # Fetch products from API
    products = fetch_best_sellers(slug)

    # Check product count and fallback if necessary
    if not products or len(products) < MIN_PRODUCTS:
        print(f"⚠️ Insufficient products for '{slug}', using fallback...")
        fallback_all = get_fallback_products(slug)
        # Randomly pick fallback products to rotate content
        products = random.sample(fallback_all, min(FALLBACK_SELECT_COUNT, len(fallback_all)))

    # Prepare and generate content
    markdown = generate_markdown(products, title)
    html = generate_html(
        products,
        category_title=title,
        template_path="templates/post.html",
        category_description=description,
    )

    html_filename = f"post-{slug}.html"
    save_blog_files(title, markdown, html, html_filename)

    # Add filename to category dict for index links
    category['filename'] = html_filename

# Generate homepage index with updated categories including filenames
generate_index_html(categories)

print("✅ Blog generation complete.")
