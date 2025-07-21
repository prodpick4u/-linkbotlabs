def generate_blog_post(products):
    blog = "# Top 3 Recommended Products\n\n"
    for i, p in enumerate(products, 1):
        blog += f"**{i}. {p['title']}**\nPrice: {p['price']}\n[Buy Now]({p['url']})\n\n"
    with open("docs/index.md", "w") as f:
        f.write(blog)
    return blog

def write_to_blog(content):
    with open("index.md", "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ Blog post written to index.md")
