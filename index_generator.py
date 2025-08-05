import os
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

def generate_index_html():
    output_path = "docs/index.html"

    # Create docs folder if it doesn't exist
    os.makedirs("docs", exist_ok=True)

    # Skip overwrite if index.html exists
    if os.path.exists(output_path):
        print(f"⚠️ Skipping index.html – file already exists at {output_path}")
        return

    try:
        env = Environment(loader=FileSystemLoader("templates"))
        template = env.get_template("index_template.html")
    except TemplateNotFound:
        print("❌ Template 'index_template.html' not found in 'templates/' folder!")
        return

    categories = [
        {"slug": "beauty", "name": "Beauty"},
        {"slug": "health", "name": "Health"},
        {"slug": "home-decor", "name": "Home Decor"},
        {"slug": "kitchen", "name": "Kitchen"},
        {"slug": "outdoors", "name": "Outdoors"},
        {"slug": "tech", "name": "Tech"},
    ]

    html = template.render(
        title="Prodpick – Amazon Blog Demo",
        categories=categories
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ Created {output_path}")
