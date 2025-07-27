import os
from jinja2 import Environment, FileSystemLoader

def generate_markdown(products, category_title):
    markdown = f"# {category_title}\n\n"
    for product in products:
        markdown += f"## [{product['title']}]({product['link']})\n"
        markdown += f"- **Price:** {product['price']}\n"
        markdown += f"- **Description:** {product['description']}\n\n"
    return markdown

def generate_html(products, category_title, template_path, category_description=""):
    env = Environment(loader=FileSystemLoader("templates"))
    template_name = os.path.basename(template_path)
    template = env.get_template(template_name)
    return template.render(
        category_title=category_title,
        products=products,
        category_description=category_description
    )

def save_blog_files(category_title, markdown, html, html_filename):
    slug = html_filename.replace(".html", "")
    md_filename = f"posts/blog_{slug}.md"
    html_output_path = f"docs/posts/{html_filename}"

    # Save markdown
    with open(md_filename, "w", encoding="utf-8") as f:
        f.write(markdown)

    # Save HTML
    with open(html_output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"📝 Saved Markdown: {md_filename}")
    print(f"🌐 Saved HTML: {html_output_path}")
