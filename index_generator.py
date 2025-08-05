import os
from jinja2 import Environment, FileSystemLoader

def generate_index_html():
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("index_template.html")

    html = template.render(
        title="Prodpick – Amazon Blog Demo",
        categories=["beauty", "health", "home-decor", "kitchen", "outdoors", "tech"]
    )

    output_path = "docs/index.html"

    if os.path.exists(output_path):
        print("⚠️  Skipping index.html – already exists.")
    else:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)
        print("✅ Created index.html")
