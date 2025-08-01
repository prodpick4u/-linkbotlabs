import os
import json
from fetch_best_sellers import fetch_best_sellers
from blog_generator import generate_markdown, save_blog_files, generate_html
from index_generator import generate_index_html
from fallback_products import get_fallback_products
from dotenv import load_dotenv

# === Load environment variables ===
if os.path.exists(".env"):
    load_dotenv()
    print("🔧 Loaded environment from .env")

# === CATEGORIES TO GENERATE ===
categories = [
    {
        "slug": "kitchen",
        "title": "Top Kitchen Gadgets on Amazon",
        "description": "Explore the best kitchen tools, appliances, and gadgets trending now."
    },
    {
        "slug": "outdoors",
        "title": "Outdoor Gear Must-Haves",
        "description": "Gear up for your next adventure with these outdoor best sellers."
    },
    {
        "slug": "beauty",
        "title": "Amazon Beauty Best Sellers",
        "description": "Discover the most loved beauty and skincare products."
    },
    {
        "slug": "home-decor",
        "title": "Stylish Home Decor on Amazon",
        "description": "Add a touch of charm to your home with these decorative finds."
    },
    {
        "slug": "tech",
        "title": "Best Tech Gadgets 2025",
        "description": "From smart devices to must-have accessories, here's what's trending in tech."
    },
    {
        "slug": "health",
        "title": "Health & Wellness Picks",
        "description": "Stay healthy and fit with these top-rated wellness products."
    },
]

# === LOOP THROUGH CATEGORIES AND GENERATE BLOG POSTS ===
for category in categories:
    slug = category["slug"]
    title = category["title"]
    description = category["description"]

    print(f"🚀 Generating blog for: {slug}")

    # Try fetching real product data from API
    products = fetch_best_sellers(slug)

    # Fallback if no products found
    if not products:
        print(f"⚠️  Using fallback products for: {slug}")
        products = get_fallback_products(slug)

    # Generate content
    markdown = generate_markdown(products, title)
    html = generate_html(
        products,
        category_title=title,
        template_path="templates/post.html",  # ✅ Shared clean template
        category_description=description
    )

    html_filename = f"post-{slug}.html"
    save_blog_files(title, markdown, html, html_filename)

# === GENERATE HOMEPAGE INDEX ===
generate_index_html(categories)

print("✅ Blog generation complete.")
