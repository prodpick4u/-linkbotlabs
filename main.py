import os
import json
import requests
from fetch_best_sellers import fetch_best_sellers
from blog_generator import generate_markdown, save_blog_files, generate_html
from index_generator import generate_index_html
from fallback_products import get_fallback_products
from dotenv import load_dotenv

# === Load environment variables (local .env for development) ===
if os.path.exists(".env"):
    load_dotenv()
    print("🔧 Loaded environment from .env")

# === Environment variables ===
# In GitHub Actions, these should be injected via env: section
APIFY_API_KEY = os.getenv("APIFY_API_KEY")
APIFY_ACTOR_ID = os.getenv("APIFY_ACTOR_ID", "V8SFJw3gKgULelpok")

SEARCH_QUERIES = [
    "top kitchen gadgets 2025",
    "best outdoor gear 2025",
    "top beauty products 2025",
    "trending tech gadgets 2025",
    "top health wellness products 2025",
    "latest home decor trends 2025"
]

def validate_apify_token():
    """Sanity-check that the Apify token works before running anything."""
    if not APIFY_API_KEY:
        print("❌ ERROR: APIFY_API_KEY is missing. Please set it in GitHub Actions secrets or your .env file.")
        return False
    response = requests.get(f"https://api.apify.com/v2/actor-runs?token={APIFY_API_KEY}")
    if response.status_code == 200:
        print("✅ Apify token is valid.")
        return True
    print(f"❌ Invalid Apify token ({response.status_code}): {response.text}")
    return False

def run_apify_google_search_scraper():
    """Triggers Apify Google Search Scraper and saves results locally."""
    url = f"https://api.apify.com/v2/acts/epctex~google-search-scraper/run-sync-get-dataset-items?token={APIFY_API_KEY}"
    payload = {
        "queries": SEARCH_QUERIES,
        "resultsPerPage": 1,
        "numPages": 1
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        with open("apify_results.json", "w", encoding="utf-8") as f:
            json.dump(response.json(), f, ensure_ascii=False, indent=2)
        print("🚀 Apify Google Search results saved to apify_results.json.")
    else:
        print(f"❌ Apify scraper failed: {response.status_code}")
        print(response.text)

def clean_docs_root_posts():
    docs_root = "docs"
    posts_dir = os.path.join(docs_root, "posts")
    os.makedirs(posts_dir, exist_ok=True)
    for filename in os.listdir(docs_root):
        if filename.startswith("post-") and filename.endswith(".html"):
            os.remove(os.path.join(docs_root, filename))
    print(f"✅ Cleaned up docs root and ensured {posts_dir} exists.")

def load_apify_keywords(filename="apify_results.json"):
    if not os.path.exists(filename):
        print("⚠️ Apify results file not found.")
        return {}

    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    keyword_map = {}
    for item in data:
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
    print("🟢 Starting blog generator pipeline...")

    # 0. Validate Apify token first
    if not validate_apify_token():
        exit(1)

    # 1. Run Apify Google Search Scraper
    run_apify_google_search_scraper()

    # 2. Clean old blog posts
    clean_docs_root_posts()

    # 3. Category list
    categories = [
        {"title": "Top Kitchen Picks 2025", "slug": "kitchen", "filename": "post-kitchen.html", "description": "Discover the top trending kitchen gadgets and appliances in 2025."},
        {"title": "Top Outdoor Essentials 2025", "slug": "outdoors", "filename": "post-outdoors.html", "description": "Explore must-have outdoor gear for 2025."},
        {"title": "Top Beauty Products 2025", "slug": "beauty", "filename": "post-beauty.html", "description": "Uncover the most loved beauty products in 2025."},
        {"title": "Top Tech Gadgets 2025", "slug": "tech", "filename": "post-tech.html", "description": "Discover the coolest tech gadgets and accessories trending in 2025."},
        {"title": "Top Health & Wellness 2025", "slug": "health", "filename": "post-health.html", "description": "Explore popular health and wellness products for your lifestyle."},
        {"title": "Top Home Decor Picks 2025", "slug": "home-decor", "filename": "post-home-decor.html", "description": "Find the latest home decor trends and stylish essentials for 2025."}
    ]

    # 4. Load Apify keyword map
    keyword_map = load_apify_keywords()

    # 5. Fetch products
    products_map = {}
    for category in categories:
        slug = category["slug"]
        search_keyword = keyword_map.get(slug, slug)
        print(f"🔍 Fetching products for category: {slug} using keyword: {search_keyword}")
        products = fetch_best_sellers(category=search_keyword, limit=3)
        if not products:
            print(f"⚠️ No API products for {slug}, using fallback.")
            products = get_fallback_products(slug)
        products_map[slug] = products

    # 6. Generate blog posts
    os.makedirs("docs/posts", exist_ok=True)
    os.makedirs("posts", exist_ok=True)
    for category in categories:
        title = category["title"]
        slug = category["slug"]
        description = category["description"]
        products = products_map.get(slug, [])
        if not products:
            print(f"⚠️ Skipping blog for {slug} (no products).")
            continue
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

    # 7. Generate index.html
    generate_index_html(
        categories,
        template_path="templates/index-template.html",
        output_path="docs/index.html"
    )

    # 8. Copy CSS
    if os.path.exists("styles.css"):
        with open("styles.css", "r", encoding="utf-8") as src, open("docs/styles.css", "w", encoding="utf-8") as dst:
            dst.write(src.read())
        print("🎨 Copied styles.css to docs/")

    print("🎉 Done! Blog and homepage ready in /docs/")
