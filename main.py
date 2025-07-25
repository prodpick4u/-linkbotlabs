import os
from fetch_best_sellers import fetch_best_sellers
from blog_generator import generate_markdown, save_blog_files, generate_html
from index_generator import generate_index_html


# === Categories metadata ===
categories = [
    {
        "title": "Top Kitchen Gadgets 2025",
        "slug": "kitchen",
        "description": "Discover the top trending kitchen gadgets and appliances in 2025. From smart tools to time-saving helpers, upgrade your cooking game today."
    },
    {
        "title": "Top Outdoor Essentials 2025",
        "slug": "outdoors",
        "description": "Explore must-have outdoor gear for 2025. Whether you’re camping, hiking, or just enjoying nature — these picks have you covered."
    },
    {
        "title": "Top Beauty Products 2025",
        "slug": "beauty",
        "description": "Uncover the most loved beauty products in 2025. From skincare to cosmetics — enhance your self-care routine with trending picks."
    }
]

# === Fetch live product data from API ===
products_map = {}
for category in categories:
    slug = category["slug"]
    print(f"🔍 Fetching products for category: {slug}")
    products = fetch_best_sellers(category=slug, limit=3)
    products_map[slug] = products

# === Ensure output directories exist ===
os.makedirs("docs", exist_ok=True)
os.makedirs("docs/posts", exist_ok=True)
os.makedirs("posts", exist_ok=True)

# === Generate blog posts with specific templates ===

# Kitchen
kitchen_products = products_map.get("kitchen", [])
if kitchen_products:
    kitchen_markdown = generate_markdown(kitchen_products, "Top Kitchen Picks 2025")
    kitchen_html = generate_html(
        kitchen_products,
        "Top Kitchen Picks 2025",
        "templates/post-kitchen-template.html",
        "Discover the top trending kitchen gadgets and appliances in 2025."
    )
    save_blog_files("Top Kitchen Picks 2025", kitchen_markdown, kitchen_html, "docs/posts/post-kitchen.html")
    print("✅ Generated blog for: Top Kitchen Picks 2025")

# Outdoors
outdoor_products = products_map.get("outdoors", [])
if outdoor_products:
    outdoor_markdown = generate_markdown(outdoor_products, "Top Outdoor Essentials 2025")
    outdoor_html = generate_html(
        outdoor_products,
        "Top Outdoor Essentials 2025",
        "templates/post-outdoor-template.html",
        "Explore must-have outdoor gear for 2025."
    )
    save_blog_files("Top Outdoor Essentials 2025", outdoor_markdown, outdoor_html, "docs/posts/post-outdoor.html")
    print("✅ Generated blog for: Top Outdoor Essentials 2025")

# Beauty
beauty_products = products_map.get("beauty", [])
if beauty_products:
    beauty_markdown = generate_markdown(beauty_products, "Top Beauty Products 2025")
    beauty_html = generate_html(
        beauty_products,
        "Top Beauty Products 2025",
        "templates/post-beauty-template.html",
        "Uncover the most loved beauty products in 2025."
    )
    save_blog_files("Top Beauty Products 2025", beauty_markdown, beauty_html, "docs/posts/post-beauty.html")
    print("✅ Generated blog for: Top Beauty Products 2025")

# === Generate homepage ===
generate_index_html(
    categories,
    template_name="index-template.html",  # only the filename, not the full path
    output_path="docs/index.html"
)

# === Copy CSS to /docs folder for GitHub Pages ===
if os.path.exists("styles.css"):
    with open("styles.css", "r", encoding="utf-8") as src, open("docs/styles.css", "w", encoding="utf-8") as dst:
        dst.write(src.read())
    print("🎨 styles.css copied to docs/")

print("🎉 All done! Homepage and blog posts generated in /docs/ for GitHub Pages.")
