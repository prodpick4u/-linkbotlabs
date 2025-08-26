import os
from jinja2 import Environment, FileSystemLoader
from fallback_products import get_fallback_products

def generate_blog_posts_from_fallback(template_path="templates/post-template.html", output_dir="docs"):
    # Load fallback products
    categories = get_fallback_products()

    # Setup Jinja2 environment
    template_dir = os.path.dirname(template_path)
    template_file = os.path.basename(template_path)
    env = Environment(loader=FileSystemLoader(template_dir or "."))
    template = env.get_template(template_file)

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    for category, products in categories.items():
        filename = f"post-{category}.html"
        output_path = os.path.join(output_dir, filename)
        rendered = template.render(category_title=category.replace("-", " ").title(), products=products)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(rendered)

        print(f"✅ Generated: {output_path}")

if __name__ == "__main__":
    generate_blog_posts_from_fallback()
