import os

def generate_markdown(products, category_title):
    markdown = f"# Top 3 {category_title} Products\n\n"
    for product in products:
        markdown += f"## [{product['title']}]({product['link']})\n"
        markdown += f"- **Price:** {product['price']}\n\n"
    return markdown

def generate_html(products, category_title, template_path):
    if not os.path.exists(template_path):
        print(f"❌ Template not found: {template_path}")
        return f"<h1>{category_title}</h1><p>No template found.</p>"

    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    product_html = ""
    for product in products:
        product_html += f"""
        <h2>{product['title']}</h2>
        <p><strong>Price:</strong> {product['price']}</p>
        <p><a href="{product['link']}" target="_blank" rel="noopener noreferrer">View on Amazon</a></p>
        <hr>
        """

    html = template.replace("{{ category_title }}", category_title)
    html = html.replace("{{ product_list }}", product_html)
    return html

def save_blog_files(category_title, markdown, html, html_output_path):
    # Ensure posts folder exists
    if not os.path.exists("posts"):
        os.makedirs("posts")
        print("📁 Created folder: posts")

    # Save markdown
    markdown_filename = os.path.join("posts", f"blog_{category_title.lower()}.md")
    with open(markdown_filename, "w", encoding="utf-8") as f:
        f.write(markdown)
    print(f"✅ Markdown saved to {markdown_filename}")

    # Save html
    with open(html_output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ HTML saved to {html_output_path}")

    # Optionally update docs/index.md for GitHub Pages
    if not os.path.exists("docs"):
        os.makedirs("docs")
    with open("docs/index.md", "w", encoding="utf-8") as f:
        f.write(markdown)
    print("✅ Updated docs/index.md (for GitHub Pages)")

def generate_index_html(categories, template_path, output_path):
    if not os.path.exists(template_path):
        print(f"❌ Template not found: {template_path}")
        return

    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    links_html = ""
    for category in categories:
        cat = category["folder"]
        title = category["title"]
        links_html += f'<li><a href="posts/post-{cat}.html">{title}</a></li>\n'

    final_html = template.replace("{{ category_links }}", links_html)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_html)
    print(f"✅ index.html saved to {output_path}")
