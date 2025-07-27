import os
import re
from jinja2 import Environment, FileSystemLoader
from fallback_products import get_fallback_products

# Slugify helper
def slugify(text):
    return re.sub(r'[^a-z0-9-]', '', text.lower().replace(" ", "-"))

# Fake API fetch (replace this with your real one)
def fetch_from_api(category):
    # ❗ Replace this with actual API logic
    return []  # simulate empty API data

# Handles API + fallback
def fetch_products(category):
    try:
        products = fetch_from_api(category)
        if not products:
            raise Exception("Empty API response")
        return products
    except Exception as e:
        print(f"⚠️ API failed for '{category}', using fallback. Reason: {e}")
        return get_fallback_products(category)

# Markdown generator
def generate_markdown(products, category_title):
    markdown = f"# Top 3 {category_title} Products\n\n"
    for product in products:
        markdown += f"## [{product['title']}]({product['link']})\n"
        markdown += f"- **Price:** {product['price']}\n\n"
    return markdown

# HTML generator
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

# Save Markdown + HTML files
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

# Generate homepage index
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

# 🚀 Entry point
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
