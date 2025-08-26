def generate_blog_post(products):
    if not products:
        print("⚠️ No products found.")
        return ""

    blog = "# 🛍️ Top 3 Recommended Products\n\n"
    for i, p in enumerate(products, 1):
        blog += f"### {i}. {p['title']}\n"
        blog += f"**Price**: {p['price']}\n\n"

        if p.get("rating"):
            blog += f"**Rating**: {p['rating']}\n\n"

        if p.get("image"):
            blog += f"![{p['title']}]({p['image']})\n\n"

        if p.get("pros"):
            blog += f"**Pros**: {p['pros']}\n\n"

        if p.get("cons"):
            blog += f"**Cons**: {p['cons']}\n\n"

        # Fallback for 'url' vs 'link'
        product_link = p.get("link") or p.get("url") or "#"
        blog += f"[👉 Buy Now on Amazon]({product_link})\n\n"
        blog += "---\n\n"

    # Write to file
    write_to_blog(blog)
    return blog

def write_to_blog(content):
    """
    Writes the blog content to the correct GitHub Pages directory.
    """
    with open("docs/index.md", "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ Blog post written to docs/index.md")
