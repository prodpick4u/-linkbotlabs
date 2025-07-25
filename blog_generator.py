import os
from jinja2 import Environment, FileSystemLoader

def generate_markdown(products, category_title):
    markdown = f"# Top 3 {category_title} Products\n\n"
    for product in products:
        markdown += f"## [{product['title']}]({product['link']})\n"
        markdown += f"- **Price:** {product['price']}\n\n"
    return markdown

def generate_html(products, category_title, template_path, category_description=""):
    if not os.path.exists(template_path):
        print(f"❌ Template not found: {template_path}")
        return f"<h1>{category_title}</h1><p>No template found.</p>"

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

def save_blog_files(category_title, markdown, html, html_output_path):
    if not os.path.exists("posts"):
        os.makedirs("posts")
        print("📁 Created folder: posts")

    safe_title = category_title.lower().replace(" ", "_")
    markdown_filename = os.path.join("posts", f"blog_{safe_title}.md")
    with open(markdown_filename, "w", encoding="utf-8") as f:
        f.write(markdown)
    print(f"✅ Markdown saved to {markdown_filename}")

    with open(html_output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ HTML saved to {html_output_path}")

    if not os.path.exists("docs"):
        os.makedirs("docs")
    with open("docs/index.md", "w", encoding="utf-8") as f:
        f.write(markdown)
    print("✅ Updated docs/index.md (for GitHub Pages)")

def generate_index_html(categories, template_path, output_path):
    if not os.path.exists(template_path):
        print(f"❌ Missing template: {template_path}")
        return

    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    post_links_html = "<ul>\n"
    for category in categories:
        slug = category.get("slug") or category.get("folder") or "unknown"
        title = category.get("title", "No Title")
        filename = f"post-{slug}.html"
        post_links_html += f'<li><a href="posts/{filename}">👉 {title}</a></li>\n'
    post_links_html += "</ul>"

    html = template.replace("{{POST_LINKS}}", post_links_html)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ Homepage saved to {output_path}")
