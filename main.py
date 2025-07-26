import os
from fetch_best_sellers import fetch_best_sellers
from blog_generator import generate_markdown, save_blog_files, generate_html
from index_generator import generate_index_html

def clean_docs_root_posts():
    docs_root = "docs"
    posts_dir = os.path.join(docs_root, "posts")

    # Ensure posts directory exists
    os.makedirs(posts_dir, exist_ok=True)

    # Remove any post-*.html files directly in docs root (misplaced files)
    for filename in os.listdir(docs_root):
        if filename.startswith("post-") and filename.endswith(".html"):
            file_path = os.path.join(docs_root, filename)
            print(f"🧹 Removing misplaced file: {file_path}")
            os.remove(file_path)

    print(f"✅ Cleaned up docs root and ensured {posts_dir} exists.")

if __name__ == "__main__":
    # Clean misplaced post files before generation
    clean_docs_root_posts()

    # === Categories metadata ===
    categories = [
        {
            "title": "Top Kitchen Picks 2025",
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

    # === Fetch products ===
    products_map = {}
    for category in categories:
        slug = category["slug"]
        print(f"🔍 Fetching products for category: {slug}")
        products = fetch_best_sellers(category=slug, limit=3)
        products_map[slug] = products

    # === Ensure output directories ===
    os.makedirs("docs", exist_ok=True)
    os.makedirs("docs/posts", exist_ok=True)
    os.makedirs("posts", exist_ok=True)

    # === Generate blog posts for each category ===
    for category in categories:
        title = category["title"]
        slug = category["slug"]
        description = category["description"]
        products = products_map.get(slug, [])

        if not products:
            print(f"⚠️ No products found for {slug}. Using fallback.")
            continue

        print(f"✍️ Generating blog for: {title}")
        
        markdown = generate_markdown(products, title)
        html = generate_html(
            products,
            category_title=title,
            template_path=f"templates/post-{slug}-template.html",
            category_description=description
        )

        save_blog_files(
            category_title=title,
            markdown=markdown,
            html=html,
            html_filename=f"docs/posts/post-{slug}.html"  # ✅ Fixed path here
        )

        print(f"✅ Blog generated for: {title}")

    # === Generate homepage index ===
    generate_index_html(
        categories,
        template_path="templates/index-template.html",
        output_path="docs/index.html"
    )

    # === Copy CSS to docs folder for GitHub Pages ===
    if os.path.exists("styles.css"):
        with open("styles.css", "r", encoding="utf-8") as src, open("docs/styles.css", "w", encoding="utf-8") as dst:
            dst.write(src.read())
        print("🎨 styles.css copied to docs/")

    print("🎉 All done! Homepage and blog posts generated in /docs/ for GitHub Pages.")
