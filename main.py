import os
from fetch_best_sellers import fetch_best_sellers
from blog_generator import generate_markdown, save_blog_files
from index_generator import generate_index_html
from jinja2 import Environment, FileSystemLoader

# === Setup Jinja2 ===
env = Environment(loader=FileSystemLoader("templates"))

def render_template(template_path, context):
    template = env.get_template(template_path)
    return template.render(context)

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

# === Generate blog posts for each category ===
for category in categories:
    slug = category["slug"]
    title = category["title"]
    description = category["description"]
    products = products_map.get(slug, [])

    if not products:
        print(f"⚠️ No products found for {title}, skipping blog generation.")
        continue

    markdown = generate_markdown(products, title)

    html = render_template(
        "post-template.html",
        {
            "category_title": title,
            "category_description": description,
            "products": products,
        }
    )

    output_path = f"posts/post-{slug}.html"
    save_blog_files(title, markdown, html, output_path)
    print(f"✅ Generated blog for: {title}")

# === Generate homepage ===
generate_index_html(
    categories,
    template_path="index-template.html",
    output_path="index.html"
)

print("🎉 All done! Homepage and blog posts generated successfully.")
