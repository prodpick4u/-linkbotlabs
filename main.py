import os
import json
from blog_generator import generate_markdown, save_blog_files, generate_html
from index_generator import generate_index_html
from fallback_products import get_fallback_products
from dotenv import load_dotenv

# === Load environment variables (local .env for development) ===
if os.path.exists(".env"):
    load_dotenv()
    print("🔧 Loaded environment from .env")

# === Target categories ===
CATEGORIES = ["beauty", "health", "home-decor", "kitchen", "outdoors", "tech"]

# === Initialize content storage ===
all_posts = []

for category in CATEGORIES:
    print(f"⚙️ Processing category: {category}")

    # Fallback only mode
    products = get_fallback_products(category)

    if not products or len(products) < 3:
        print(f"⚠️ Using fallback products for {category}")
        products = get_fallback_products(category)

    # === Generate blog content ===
    markdown, html = generate_markdown(products, category), generate_html(products, category)
    save_blog_files(markdown, html, category)
    all_posts.append({
        "category": category,
        "filename": f"post-{category}.html"
    })

# === Generate main index.html ===
index_html = generate_index_html(all_posts)
index_path = os.path.join("docs", "index.html")

with open(index_path, "w", encoding="utf-8") as f:
    f.write(index_html)
    print(f"✅ index.html generated at: {index_path}")
