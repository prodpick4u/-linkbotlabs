import os
from blog_generator import generate_blog_post
from html_generator import render_html_from_template

# Define your categories here
CATEGORIES = ["beauty", "health", "home-decor", "kitchen", "outdoors", "tech"]

# Set directories
DOCS_DIR = "docs"
TEMPLATE_DIR = "templates"
HTML_TEMPLATE = "post_template.html"  # Your post HTML template

# Ensure output directory exists
os.makedirs(DOCS_DIR, exist_ok=True)

for category in CATEGORIES:
    print(f"⚙️ Processing category: {category}")

    # Generate blog content in markdown and extract product data
    markdown_content, context = generate_blog_post(category)

    # Save markdown
    markdown_path = os.path.join(DOCS_DIR, f"blog_post-{category}.md")
    with open(markdown_path, "w", encoding="utf-8") as md_file:
        md_file.write(markdown_content)
        print(f"📝 Saved Markdown: {markdown_path}")

    # Render and save HTML post
    html_output_path = os.path.join(DOCS_DIR, f"post-{category}.html")
    render_html_from_template(
        template_name=HTML_TEMPLATE,
        context=context,
        output_path=html_output_path
    )
    print(f"🌐 Saved HTML: {html_output_path}")

print("✅ All blog posts generated. index.html was not touched.")
