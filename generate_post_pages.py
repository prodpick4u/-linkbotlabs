import os

# Sample product data for 3 categories
categories = {
    "kitchen": {
        "title": "Top Kitchen Gadgets for 2025",
        "description": "Top-rated kitchen picks to enhance your cooking.",
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
    },
    "outdoors": {
        "title": "Top Outdoor Gear for 2025",
        "description": "Our favorite tools for adventure and travel.",
        "filename": "post-outdoors.html",
        "products": [
            {
                "title": "Coleman Sundome Tent",
                "image": "https://example.com/outdoor1.jpg",
                "price": "$69.99",
                "pros": "Easy setup, Waterproof",
                "cons": "Not great for winter",
                "link": "https://www.amazon.com/dp/B0009PUSPI"
            },
            {
                "title": "LifeStraw Water Filter",
                "image": "https://example.com/outdoor2.jpg",
                "price": "$19.95",
                "pros": "Portable, Affordable",
                "cons": "Slow filtration",
                "link": "https://www.amazon.com/dp/B006QF3TW4"
            },
            {
                "title": "Garmin GPS Handheld",
                "image": "https://example.com/outdoor3.jpg",
                "price": "$129.99",
                "pros": "Accurate tracking, Durable",
                "cons": "Small screen",
                "link": "https://www.amazon.com/dp/B01MRZ0H7T"
            },
        ]
    },
    "beauty": {
        "title": "Best Beauty Tools for 2025",
        "description": "Beauty essentials our readers swear by.",
        "filename": "post-beauty.html",
        "products": [
            {
                "title": "Revlon Hair Dryer Brush",
                "image": "https://example.com/beauty1.jpg",
                "price": "$59.99",
                "pros": "Volumizes, Quick drying",
                "cons": "Bulky to store",
                "link": "https://www.amazon.com/dp/B01LSUQSB0"
            },
            {
                "title": "Neutrogena Hydro Boost Gel",
                "image": "https://example.com/beauty2.jpg",
                "price": "$16.99",
                "pros": "Lightweight, Hydrating",
                "cons": "Not great for very dry skin",
                "link": "https://www.amazon.com/dp/B00NR1YQK4"
            },
            {
                "title": "Olaplex Hair Perfector No. 3",
                "image": "https://example.com/beauty3.jpg",
                "price": "$28.00",
                "pros": "Repairs damaged hair, Smells good",
                "cons": "Expensive for size",
                "link": "https://www.amazon.com/dp/B00SNM5US4"
            },
        ]
    }
}

# Load the post template
with open("posts/post-template.html", "r", encoding="utf-8") as f:
    post_template = f.read()

# Ensure the docs directory exists
os.makedirs("docs", exist_ok=True)

# Generate HTML for each category
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

    final_html = post_template.replace("{{ category_title }}", cat_data["title"])
    final_html = final_html.replace("{{ category_description }}", cat_data["description"])
    final_html = final_html.replace("{{ product_list }}", product_cards)

    filepath = os.path.join("docs", cat_data["filename"])
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(final_html)

    print(f"✅ Generated: {filepath}")
