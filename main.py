import os
from blog_generator import generate_markdown, save_blog_files, generate_html
from index_generator import generate_index_html
from fallback_products import get_fallback_products
from dotenv import load_dotenv

if os.path.exists(".env"):
    load_dotenv()
    print("🔧 Loaded environment from .env")

categories = [
    {"slug": "beauty", "title": "Amazon Beauty Best Sellers", "description": "Discover the most loved beauty and skincare products."},
    {"slug": "health", "title": "Health & Wellness Picks", "description": "Stay healthy and fit with these top-rated wellness products."},
    {"slug": "home-decor", "title": "Stylish Home Decor on Amazon", "description": "Add a touch of charm to your home with these decorative finds."},
    {"slug": "kitchen", "title": "Top Kitchen Gadgets on Amazon", "description": "Explore the best kitchen tools, appliances, and gadgets trending now."},
    {"slug": "outdoors", "title": "Outdoor Gear Must-Haves", "description": "Gear up for your next adventure with these outdoor best sellers."},
    {"slug": "tech", "title": "Best Tech Gadgets 2025", "description": "From smart devices to must-have accessories, here's what's trending in tech."},
]

all_posts = []

def write_html_file(filename, content):
    if filename == "index.html":
        print("⚠️ Skipping overwrite of docs/index.html to preserve custom homepage.")
        return
    os.makedirs("docs", exist_ok=True)
    path = os.path.join("docs", filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Saved {path}")

for cat in categories:
    slug = cat["slug"]
    title = cat["title"]
    description = cat["description"]

    print(f"⚙️ Processing category: {slug}")

    products = get_fallback_products(slug)

    markdown = generate_markdown(products, title)
    html = generate_html(
        products,
        category_title=title,
        category_description=description,
        template_path="templates/post.html"
    )

    filename = f"post-{slug}.html"
    save_blog_files(title, markdown, html, filename)

    all_posts.append({
        "category": title,
        "filename": filename
    })

# Generate index HTML but DO NOT overwrite docs/index.html
# If you want to update index.html manually, skip this call or modify generate_index_html accordingly.
print("⚠️ Skipping automated index.html generation to avoid overwrite.")
# If you want, comment out the next line:
# generate_index_html(all_posts)
