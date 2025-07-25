import os
from fetch_best_sellers import fetch_best_sellers
from blog_generator import generate_markdown, generate_html, save_blog_files
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
    html = generate_html(
        products,
        category_title=title,
        category_description=description,
        template_path="posts/post-template.html"
    )

    output_path = f"posts/post-{slug}.html"
    save_blog_files(title, markdown, html, output_path)
    print(f"✅ Generated blog for: {title}")

# === Generate homepage with links to blogs ===
generate_index_html(
    categories,
    template_path="index-template.html",
    output_path="index.html"
)

print("🎉 All done! Homepage and blog posts generated successfully.")
