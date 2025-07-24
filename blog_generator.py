import os

def generate_markdown(products, category):
    if not products:
        print("⚠️ No products found. Using default markdown products.")
        products = [
            {"title": "Sample Product A", "price": "$29.99", "link": "https://www.amazon.com/dp/sampleA"},
            {"title": "Sample Product B", "price": "$49.99", "link": "https://www.amazon.com/dp/sampleB"},
            {"title": "Sample Product C", "price": "$19.99", "link": "https://www.amazon.com/dp/sampleC"},
        ]

    blog = f"# 🛍️ Top 3 {category.title()} Picks\n\n"
    for i, p in enumerate(products, 1):
        blog += f"### {i}. {p['title']}\n"
        blog += f"**Price**: {p.get('price', 'N/A')}\n\n"
        if p.get("rating"):
            blog += f"**Rating**: {p['rating']}\n\n"
        if p.get("image"):
            blog += f"![{p['title']}]({p['image']})\n\n"
        if p.get("pros"):
            blog += f"**Pros**: {p['pros']}\n\n"
        if p.get("cons"):
            blog += f"**Cons**: {p['cons']}\n\n"
        blog += f"[👉 Buy Now on Amazon]({p['link']})\n\n"
        blog += "---\n\n"
    return blog

def generate_html(products, category, template_path):
    if not os.path.exists(template_path):
        print(f"❌ Template file not found: {template_path}")
        return ""

    try:
        with open(template_path, "r", encoding="utf-8") as file:
            template = file.read()
    except Exception as e:
        print(f"❌ Error reading HTML template: {e}")
        return ""

    product_html = ""
    for p in products:
        card = f"""
        <div class="product-card">
            <h2>{p.get('title')}</h2>
            <p><strong>Price:</strong> {p.get('price', 'N/A')}</p>
        """
        if p.get("image"):
            card += f"<img src='{p['image']}' alt='{p['title']}' style='max-width:300px;'/>"
        if p.get("rating"):
            card += f"<p><strong>Rating:</strong> {p['rating']}</p>"
        if p.get("pros"):
            card += f"<p><strong>Pros:</strong> {p['pros']}</p>"
        if p.get("cons"):
            card += f"<p><strong>Cons:</strong> {p['cons']}</p>"
        card += f"<p><a href='{p['link']}'>👉 Buy on Amazon</a></p></div><hr>"
        product_html += card

    return template.replace("{{products}}", product_html).replace("{{category}}", category.title())

def save_blog_files(category, markdown, html, html_output_path):
    markdown_filename = f"blog_{category.lower()}.md"
    html_filename = html_output_path

    with open(markdown_filename, "w", encoding="utf-8") as f:
        f.write(markdown)
    print(f"✅ Markdown saved to {markdown_filename}")

    with open(html_filename, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ HTML saved to {html_filename}")

    with open("docs/index.md", "w", encoding="utf-8") as f:
        f.write(markdown)
    print("✅ Also updated docs/index.md (for GitHub Pages)")
def generate_index_html(categories):
    html = """<html>
<head><title>Top Amazon Picks</title></head>
<body>
    <h1>Top Categories</h1>
    <ul>
"""
    for category in categories:
        html += f'        <li><a href="{category["folder"]}/index.html">{category["title"]}</a></li>\n'

    html += """    </ul>
</body>
</html>"""
    return html
