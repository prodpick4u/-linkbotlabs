import os

# Sample data – this will eventually come from your scraper
categories = {
    "kitchen": {
        "title": "Top Kitchen Gadgets for 2025",
        "filename": "post-kitchen.html",
        "products": [
            {
                "title": "Ninja Air Fryer",
                "image": "https://example.com/image1.jpg",
                "price": "$99.99",
                "pros": "Cooks fast, Easy to clean, Low oil",
                "cons": "Small capacity",
                "link": "https://www.amazon.com/dp/B07YXL5GLM"
            },
            {
                "title": "Instant Pot Duo",
                "image": "https://example.com/image2.jpg",
                "price": "$89.99",
                "pros": "Multi-function, Time saving",
                "cons": "Takes counter space",
                "link": "https://www.amazon.com/dp/B08ZJTX8WZ"
            },
            {
                "title": "Hamilton Beach Blender",
                "image": "https://example.com/image3.jpg",
                "price": "$49.99",
                "pros": "Affordable, Powerful motor",
                "cons": "Loud",
                "link": "https://www.amazon.com/dp/B07PZ4PK4R"
            },
        ]
    }
    # Add outdoor and beauty later
}

# Load the post template
with open("templates/post-template.html", "r", encoding="utf-8") as f:
    post_template = f.read()

# Generate category post pages
for cat_key, cat_data in categories.items():
    product_cards = ""
    for product in cat_data["products"]:
        product_cards += f"""
        <div class="product">
          <h2>{product['title']}</h2>
          <img src="{product['image']}" alt="{product['title']}" />
          <p><strong>Price:</strong> {product['price']}</p>
          <p><strong>Pros:</strong> {product['pros']}</p>
          <p><strong>Cons:</strong> {product['cons']}</p>
          <a href="{product['link']}" target="_blank" rel="noopener noreferrer">Buy on Amazon</a>
        </div>
        """

    final_html = post_template.replace("{{PAGE_TITLE}}", cat_data["title"])
    final_html = final_html.replace("{{PRODUCT_CARDS}}", product_cards)

    os.makedirs("docs/posts", exist_ok=True)
    filepath = os.path.join("docs/posts", cat_data["filename"])
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(final_html)

    print(f"✅ Generated: {filepath}")
