import os
import json
from fetch_best_sellers import fetch_best_sellers
from blog_generator import generate_markdown, save_blog_files, generate_html
from index_generator import generate_index_html
from fallback_products import get_fallback_products

def clean_docs_root_posts():
    docs_root = "docs"
    posts_dir = os.path.join(docs_root, "posts")

    os.makedirs(posts_dir, exist_ok=True)

    for filename in os.listdir(docs_root):
        if filename.startswith("post-") and filename.endswith(".html"):
            file_path = os.path.join(docs_root, filename)
            print(f"🧹 Removing misplaced file: {file_path}")
            os.remove(file_path)

    print(f"✅ Cleaned up docs root and ensured {posts_dir} exists.")

def load_apify_keywords(filename="apify_results.json"):
    if not os.path.exists(filename):
        print("⚠️ Apify results file not found.")
        return {}

    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    keyword_map = {}
    # You may need to adjust this depending on actual structure of apify_results.json
    for item in data:
        # Assume each item has a searchQuery or query field (adjust as needed)
        query = item.get("searchQuery") or item.get("query") or ""
        query = query.lower()
        if "kitchen" in query:
            keyword_map["kitchen"] = query
        elif "outdoor" in query:
            keyword_map["outdoors"] = query
        elif "beauty" in query:
            keyword_map["beauty"] = query
        elif "tech" in query:
            keyword_map["tech"] = query
        elif "health" in query:
            keyword_map["health"] = query
        elif "home decor" in query or "home" in query:
            keyword_map["home-decor"] = query

    return keyword_map

if __name__ == "__main__":
    clean_docs_root_posts()

    categories = [
        {
            "title": "Top Kitchen Picks 2025",
            "slug": "kitchen",
            "filename": "post-kitchen.html",
            "description": "Discover the top trending kitchen gadgets and appliances in 2025. From smart tools to time-saving helpers, upgrade your cooking game today."
        },
        {
            "title": "Top Outdoor Essentials 2025",
            "slug": "outdoors",
            "filename": "post-outdoors.html",
            "description": "Explore must-have outdoor gear for 2025. Whether you’re camping, hiking, or just enjoying nature — these picks have you covered."
        },
        {
            "title": "Top Beauty Products 2025",
            "slug": "beauty",
            "filename": "post-beauty.html",
            "description": "Uncover the most loved beauty products in 2025. From skincare to cosmetics — enhance your self-care routine with trending picks."
        },
        {
            "title": "Top Tech Gadgets 2025",
            "slug": "tech",
            "filename": "post-tech.html",
            "description": "Discover the coolest tech gadgets and accessories trending in 2025."
        },
        {
            "title": "Top Health & Wellness 2025",
            "slug": "health",
            "filename": "post-health.html",
            "description": "Explore popular health and wellness products that will improve your lifestyle."
        },
        {
            "title": "Top Home Decor Picks 2025",
            "slug": "home-decor",
            "filename": "post-home-decor.html",
            "description": "Find the latest home decor trends and stylish essentials for 2025."
        }
    ]

    keyword_map = load_apify_keywords()

    products_map = {}
    for category in categories:
        slug = category["slug"]
        # Use the keyword from Apify results or fallback to slug
        search_keyword = keyword_map.get(slug, slug)
        print(f"🔍 Fetching products for category: {slug} using keyword: {search_keyword}")
        products = fetch_best_sellers(category=search_keyword, limit=3)
        if not products:
            print(f"⚠️ API fetch failed or empty for {slug}. Using fallback products.")
            products = get_fallback_products(slug)
        products_map[slug] = products

    os.makedirs("docs/posts", exist_ok=True)
    os.makedirs("posts", exist_ok=True)

    for category in categories:
        title = category["title"]
        slug = category["slug"]
        description = category["description"]
        products = products_map.get(slug, [])

        if not products:
            print(f"⚠️ No products available for {slug}, skipping blog generation.")
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
            html_filename=f"post-{slug}.html"
        )

        print(f"✅ Blog generated for: {title}")

    generate_index_html(
        categories,
        template_path="templates/index-template.html",
        output_path="docs/index.html"
    )

    if os.path.exists("styles.css"):
        with open("styles.css", "r", encoding="utf-8") as src, open("docs/styles.css", "w", encoding="utf-8") as dst:
            dst.write(src.read())
        print("🎨 styles.css copied to docs/")

    print("🎉 All done! Homepage and blog posts generated in /docs/ for GitHub Pages.")
