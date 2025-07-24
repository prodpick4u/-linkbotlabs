import os
def generate_markdown(products, category_title):
    markdown = f"# Top 3 {category_title} Products\n\n"
    for product in products:
        markdown += f"## {product['title']}\n"
        markdown += f"- **Price**: {product['price']}\n"
        markdown += f"- [View on Amazon]({product['link']})\n\n"
    return markdown
def save_blog_files(category, markdown, html, html_output_path):
    # Ensure 'posts' folder exists
    if not os.path.exists("posts"):
        os.makedirs("posts")
        print("📁 Created folder: posts")

    # Save markdown inside posts/
    markdown_filename = os.path.join("posts", f"blog_{category.lower()}.md")
    with open(markdown_filename, "w", encoding="utf-8") as f:
        f.write(markdown)
    print(f"✅ Markdown saved to {markdown_filename}")

    # Save HTML to the specified output path (should already be under posts/)
    with open(html_output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ HTML saved to {html_output_path}")

    # Optionally update docs/index.md (if using GitHub Pages)
    if not os.path.exists("docs"):
        os.makedirs("docs")
    with open("docs/index.md", "w", encoding="utf-8") as f:
        f.write(markdown)
    print("✅ Updated docs/index.md (for GitHub Pages)")
