import os

def generate_blog_index(posts_folder="docs/posts", output_file="docs/posts/index.html"):
    post_links = []
    for filename in sorted(os.listdir(posts_folder)):
        if filename.endswith(".html") and filename != "index.html":
            title = filename.replace(".html", "").replace("-", " ").title()
            post_links.append(f'<li><a href="{filename}">{title}</a></li>')

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Prodpick Blog</title>
    <style>
        body {{ font-family: Inter, sans-serif; padding: 20px; background: #f8fafc; }}
        h1 {{ color: #1f2937; }}
        ul {{ list-style-type: none; padding: 0; }}
        li {{ margin-bottom: 10px; }}
        a {{ color: #2563eb; text-decoration: none; font-weight: bold; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <h1>📝 Prodpick Blog Posts</h1>
    <ul>
        {''.join(post_links)}
    </ul>
</body>
</html>"""

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"📚 Blog index generated at: {output_file}")
