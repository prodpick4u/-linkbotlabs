def generate_index_html(categories, template_path, output_path):
    import os

    if not os.path.exists(template_path):
        print(f"❌ Template not found: {template_path}")
        return

    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    # Generate dynamic blog links
    post_links_html = "<ul>\n"
    for category in categories:
        cat = category["folder"]
        title = category["title"]
        post_links_html += f'<li><a href="posts/post-{cat}.html">{title} Top Picks</a></li>\n'
    post_links_html += "</ul>"

    # Replace the placeholder
    final_html = template.replace("{{POST_LINKS}}", post_links_html)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_html)

    print(f"✅ index.html updated with blog links → {output_path}")
