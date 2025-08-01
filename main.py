import os
import json
import time
import requests
from dotenv import load_dotenv
from fetch_best_sellers import fetch_best_sellers
from blog_generator import generate_markdown, save_blog_files, generate_html
from index_generator import generate_index_html
from fallback_products import get_fallback_products

# === Load environment variables ===
if os.path.exists(".env"):
    load_dotenv()
    print("🔧 Loaded environment from .env")

# === Environment variables ===
APIFY_TOKEN = os.getenv("APIFY_TOKEN")
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
    if not APIFY_TOKEN:
        print("❌ ERROR: APIFY_TOKEN is missing. Please set it in your .env file or GitHub secrets.")
        return False
    response = requests.get(f"https://api.apify.com/v2/actor-runs?token={APIFY_TOKEN}")
    if response.status_code == 200:
        print("✅ Apify token is valid.")
        return True
    print(f"❌ Invalid Apify token ({response.status_code}): {response.text}")
    return False

def run_apify_google_search_scraper():
    print("🚀 Triggering Apify actor...")

    run_url = f"https://api.apify.com/v2/acts/{APIFY_ACTOR_ID}/runs?token={APIFY_TOKEN}"
    payload = {
        "queries": SEARCH_QUERIES,
        "resultsPerPage": "10",
        "numPages": 1,
        "csvFriendlyOutput": False,
        "customMapFunction": "(object) => { return {...object} }",
        "proxy": {
            "useApifyProxy": True
        }
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(run_url, json=payload, headers=headers)

    if response.status_code != 201:
        print(f"❌ Apify request failed: {response.status_code}")
        print(response.text)
        return

    run_data = response.json()
    run_id = run_data.get("id")
    print(f"⏳ Waiting... Actor status: RUNNING")

    status_url = f"https://api.apify.com/v2/actor-runs/{run_id}?token={APIFY_TOKEN}"
    while True:
        status_response = requests.get(status_url)
        if status_response.status_code != 200:
            print("❌ Failed to get run status.")
            return
        status = status_response.json().get("status")
        if status in ["SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"]:
            break
        print(f"⏳ Waiting... Actor status: {status}")
        time.sleep(5)

    if status != "SUCCEEDED":
        print(f"❌ Apify actor did not complete successfully: {status}")
        return

    dataset_url = f"https://api.apify.com/v2/actor-runs/{run_id}/dataset/items?token={APIFY_TOKEN}&clean=true"
    dataset_response = requests.get(dataset_url)
    if dataset_response.status_code == 200:
        with open("apify_results.json", "w", encoding="utf-8") as f:
            json.dump(dataset_response.json(), f, ensure_ascii=False, indent=2)
        print("✅ Apify results saved to apify_results.json")
    else:
        print(f"❌ Failed to fetch dataset: {dataset_response.status_code}")

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

def fetch_products_with_fallback(slug, search_keyword):
    try:
        products = fetch_best_sellers(category=search_keyword, limit=3)
    except Exception as e:
        print(f"⚠️ API fetch error for {slug}: {e}")
        products = []
    if not products:
        print(f"⚠️ No API products for {slug}, using fallback.")
        products = get_fallback_products(slug)
    return products

if __name__ == "__main__":
    print("🟢 Starting blog generator pipeline...")

    if not validate_apify_token():
        exit(1)

    run_apify_google_search_scraper()
    clean_docs_root_posts()

    categories = [
        {"title": "Top Kitchen Picks 2025", "slug": "kitchen", "filename": "post-kitchen.html", "description": "Discover the top trending kitchen gadgets and appliances in 2025."},
        {"title": "Top Outdoor Essentials 2025", "slug": "outdoors", "filename": "post-outdoors.html", "description": "Explore must-have outdoor gear for 2025."},
        {"title": "Top Beauty Products 2025", "slug": "beauty", "filename": "post-beauty.html", "description": "Uncover the most loved beauty products in 2025."},
        {"title": "Top Tech Gadgets 2025", "slug": "tech", "filename": "post-tech.html", "description": "Discover the coolest tech gadgets and accessories trending in 2025."},
        {"title": "Top Health & Wellness 2025", "slug": "health", "filename": "post-health.html", "description": "Explore popular health and wellness products for your lifestyle."},
        {"title": "Top Home Decor Picks 2025", "slug": "home-decor", "filename": "post-home-decor.html", "description": "Find the latest home decor trends and stylish essentials for 2025."}
    ]

    keyword_map = load_apify_keywords()

    products_map = {}
    for category in categories:
        slug = category["slug"]
        search_keyword = keyword_map.get(slug, slug)
        print(f"🔍 Fetching products for category: {slug} using keyword: {search_keyword}")
        products = fetch_products_with_fallback(slug, search_keyword)
        products_map[slug] = products

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

    generate_index_html(
        categories,
        template_path="templates/index-template.html",
        output_path="docs/index.html"
    )

    if os.path.exists("styles.css"):
        with open("styles.css", "r", encoding="utf-8") as src, open("docs/styles.css", "w", encoding="utf-8") as dst:
            dst.write(src.read())
        print("🎨 Copied styles.css to docs/")

    print("🎉 Done! Blog and homepage ready in /docs/")
