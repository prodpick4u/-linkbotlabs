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
        blog += f"[👉 Buy Now on Amazon]({p['link']})\n\n"
        blog += "---\n\n"

    # Save to markdown file
    with open("docs/index.md", "w", encoding="utf-8") as f:
        f.write(blog)

    print("✅ Blog post written to `docs/index.md`")
    return blog
