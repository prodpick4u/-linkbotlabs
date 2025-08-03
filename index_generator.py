import os

def generate_index_html(all_posts, output_path="docs/index.html"):
    # all_posts is a list of dicts: [{"category": ..., "filename": ...}, ...]

    cards_html = ""
    for post in all_posts:
        title = post.get("category", "No Title")
        filename = post.get("filename", "#")
        cards_html += f'''
        <div class="card">
          <h3>{title}</h3>
          <a href="{filename}">View Post</a>
        </div>
        '''

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Prodpick4u – Amazon Blog Demo</title>
  <style>
    body {{
      background: #0a0a0a;
      color: #ffffff;
      font-family: 'Inter', sans-serif;
      margin: 0;
      padding: 0;
    }}
    header {{
      text-align: center;
      padding: 2rem;
    }}
    h1 {{
      font-size: 2rem;
      margin-bottom: 0.5rem;
    }}
    .grid {{
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: 1rem;
      padding: 1rem;
    }}
    .card {{
      background: #1e1e1e;
      border: 1px solid #333;
      border-radius: 8px;
      width: 280px;
      padding: 1rem;
      text-align: center;
      transition: all 0.2s;
    }}
    .card:hover {{
      border-color: #00ffd5;
      box-shadow: 0 0 10px #00ffd5;
    }}
    .card a {{
      color: #00ffd5;
      text-decoration: none;
      font-weight: 600;
      display: block;
      margin-top: 0.5rem;
    }}
  </style>
</head>
<body>
  <header>
    <h1>🛒 Prodpick4u Amazon Blog Demo</h1>
    <p>Explore a working sample of an automated affiliate blog powered by fallback products and Amazon links.</p>
  </header>

  <div class="grid">
    {cards_html}
  </div>

</body>
</html>"""

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ {output_path} generated successfully.")
    return html
