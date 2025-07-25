def generate_index_html(categories, template_path="templates/index-template.html", output_path="index.html"):
    # Build HTML for each category link
    links_html = "\n".join([
        f'<a href="posts/post-{cat["slug"]}.html">👉 {cat["title"]}</a>'
        for cat in categories
    ])

    # Load and render template
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    rendered = template.replace("{{POST_LINKS}}", links_html)

    # Write output file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rendered)

    print("✅ index.html generated successfully.")
