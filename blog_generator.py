def generate_index_html(categories):
    template = """
    <html>
    <head>
        <title>YouTube + Amazon Blog Generator</title>
    </head>
    <body>
        <h1>YouTube + Amazon Blog Generator</h1>
        <p>Automatically generates product review blogs with embedded YouTube videos and affiliate links.</p>

        <h2>Latest Product Categories</h2>
        {{POST_LINKS}}

        <footer>
            <p>Made by Prodpick4u</p>
        </footer>
    </body>
    </html>
    """

    # Build the links list
    post_links_html = "<ul>\n"
    for category in categories:
        post_links_html += f'<li><a href="posts/{category["filename"]}">{category["title"]}</a></li>\n'
    post_links_html += "</ul>"

    # Replace placeholder and write file
    html = template.replace("{{POST_LINKS}}", post_links_html)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("✅ index.html saved to root directory")
