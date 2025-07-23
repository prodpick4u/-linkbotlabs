def generate_blog_post(products):
    if not products:
        print("⚠️ No products found. Using default products.")
        products = [
            {
                "title": "Sample Product A",
                "price": "$29.99",
                "link": "https://www.amazon.com/dp/sampleA"
            },
            {
                "title": "Sample Product B",
                "price": "$49.99",
                "link": "https://www.amazon.com/dp/sampleB"
            },
            {
                "title": "Sample Product C",
                "price": "$19.99",
                "link": "https://www.amazon.com/dp/sampleC"
            }
        ]

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

        blog += f"[👉 Buy Now on Amazon]({p['link']})\n\n"
        blog += "---\n\n"

    with open("docs/index.md", "w", encoding="utf-8") as f:
        f.write(blog)

    print("✅ Blog post written to `docs/index.md`")
    return blog
