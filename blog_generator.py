import os
import re
import requests
from jinja2 import Environment, FileSystemLoader
from fallback_products import get_fallback_products

# Slugify helper
def slugify(text):
    return re.sub(r'[^a-z0-9-]', '', text.lower().replace(" ", "-"))

# --- Apify integration ---
def run_apify_actor(input_payload):
    actor_id = os.getenv("APIFY_ACTOR_ID", "jm4192gDoX7CHY7IB")
    token = os.getenv("APIFY_TOKEN")
    url = f"https://api.apify.com/v2/actor-tasks/{actor_id}/run-sync-get-dataset-items?token={token}"
    try:
        resp = requests.post(url, json=input_payload, timeout=60)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"❌ Apify API error: {e}")
        return []

# --- RapidAPI snippet 2 - Real-Time Product Search ---
def fetch_products_by_keyword(keyword="best kitchen gadgets", country="us", limit=3):
    url = (
        f"https://real-time-product-search.p.rapidapi.com/search-light-v2"
        f"?q={keyword}&country={country}&language=en&page=1&limit={limit}"
        f"&sort_by=BEST_MATCH&product_condition=ANY&return_filters=false"
    )
    headers = {
        "x-rapidapi-host": "real-time-product-search.p.rapidapi.com",
        "x-rapidapi-key": os.getenv("RAPIDAPI_KEY")
    }
    try:
        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
        return resp.json().get("data", {}).get("products", [])
    except Exception as e:
        print(f"❌ Real-Time Product Search API error: {e}")
        return []

# --- Fetch from API with fallback chain ---
def fetch_from_api(category):
    # 1. Try Apify first
    input_payload = {"searchTerm": category, "country": "us"}
    apify_results = run_apify_actor(input_payload)
    if apify_results:
        print(f"✅ Got {len(apify_results)} products from Apify")
        return apify_results[:3]

    # 2. If Apify fails, try RapidAPI snippet 2
    keywords_map = {
        "kitchen": "kitchen appliances",
        "outdoors": "outdoor gear",
        "beauty": "beauty products",
        "household": "household appliances"
    }
    keyword = keywords_map.get(category, category)

    rapid_results = fetch_products_by_keyword(keyword, limit=3)
    if rapid_results:
        print(f"✅ Got {len(rapid_results)} products from RapidAPI Product Search")
        return rapid_results

    # 3. No API results, raise to fallback
    raise Exception("No data from API sources")

# --- Handle API + fallback ---
def fetch_products(category):
    try:
        products = fetch_from_api(category)
        if not products:
            raise Exception("Empty API response")
        return products
    except Exception as e:
        print(f"⚠️ API failed for '{category}', using fallback. Reason: {e}")
        return get_fallback_products(category)

# --- Markdown generator ---
def generate_markdown(products, category_title):
    markdown = f"# Top 3 {category_title} Products\n\n"
    for product in products:
        # Handle possible differences in keys between APIs and fallback data
        title = product.get("title") or product.get("name") or "No title"
        link = product.get("link") or product.get("url") or "#"
        price = product.get("price") or product.get("lowestPrice") or "N/A"
        markdown += f"## [{title}]({link})\n"
        markdown += f"- **Price:** {price}\n\n"
    return markdown

# --- HTML generator ---
def generate_html(products, category_title, template_path, category_description=""):
    if not os.path.exists(template_path):
        print(f"❌ Template not found: {template_path}")
        return f"<h1>{category_title}</h1><p>No template found.</p>"

    if not products:
        return f"<h1>{category_title}</h1><p>No products available.</p>"

    template_dir = os.path.dirname(template_path)
    template_file = os.path.basename(template_path)

    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(template_file)

    html = template.render(
        category_title=category_title,
        category_description=category_description,
        products=products
    )
    return html

# --- Save Markdown + HTML files ---
def save_blog_files(category_title, markdown, html, html_filename=None):
    os.makedirs("posts", exist_ok=True)

    safe_title = slugify(category_title)
    markdown_filename = os.path.join("posts", f"blog_{safe_title}.md")
    with open(markdown_filename, "w", encoding="utf-8") as f:
        f.write(markdown)
    print(f"✅ Markdown saved to {markdown_filename}")

    if not html_filename:
        html_filename = f"post-{safe_title}.html"

    html_output_path = os.path.join("docs", "posts", html_filename)
    os.makedirs(os.path.dirname(html_output_path), exist_ok=True)
    with open(html_output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ HTML saved to {html_output_path}")

# --- Generate homepage index ---
def generate_index_html(categories, template_path="templates/index-template.html", output_path="docs/index.html"):
    if not os.path.exists(template_path):
        print(f"❌ Missing template: {template_path}")
        return

    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    post_links_html = "<ul>\n"
    for category in categories:
        slug = slugify(category.get("slug") or category.get("folder") or category.get("title", "unknown"))
        title = category.get("title", "No Title")
        filename = f"posts/post-{slug}.html"
        post_links_html += f'<li><a href="{filename}">👉 {title}</a></li>\n'
    post_links_html += "</ul>"

    html = template.replace("{{POST_LINKS}}", post_links_html)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ Homepage saved to {output_path}")

# --- Entry point ---
if __name__ == "__main__":
    categories = [
        {"title": "Kitchen Appliances", "slug": "kitchen", "template": "templates/post-kitchen-template.html"},
        {"title": "Outdoor Essentials", "slug": "outdoors", "template": "templates/post-outdoor-template.html"},
        {"title": "Beauty Products", "slug": "beauty", "template": "templates/post-beauty-template.html"},
        {"title": "Household Appliances", "slug": "household", "template": "templates/post-household-template.html"}
    ]

    for cat in categories:
        slug = cat["slug"]
        title = cat["title"]
        template = cat["template"]

        print(f"\n🚀 Generating blog for: {title}")
        products = fetch_products(slug)

        markdown = generate_markdown(products, title)
        html = generate_html(products, title, template)
        save_blog_files(title, markdown, html)

    generate_index_html(categories)
