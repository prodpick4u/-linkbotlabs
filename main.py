import os
from blog_generator import generate_markdown, generate_html, save_blog_files
from index_generator import generate_index_html

# === Categories metadata ===
categories = [
    {
        "title": "Top Kitchen Gadgets 2025",
        "slug": "kitchen",
        "description": "Discover the top trending kitchen gadgets and appliances in 2025. From smart tools to time-saving helpers, upgrade your cooking game today."
    },
    {
        "title": "Top Outdoor Essentials 2025",
        "slug": "outdoors",
        "description": "Explore must-have outdoor gear for 2025. Whether you’re camping, hiking, or just enjoying nature — these picks have you covered."
    },
    {
        "title": "Top Beauty Products 2025",
        "slug": "beauty",
        "description": "Uncover the most loved beauty products in 2025. From skincare to cosmetics — enhance your self-care routine with trending picks."
    }
]

# === Example product data ===
products_map = {
    "kitchen": [
        {"title": "Knife Set", "price": "$59.99", "link": "https://amazon.com/dp/knife"},
        {"title": "Blender", "price": "$89.99", "link": "https://amazon.com/dp/blender"},
        {"title": "Cutting Board", "price": "$19.99", "link": "https://amazon.com/dp/cuttingboard"},
    ],
    "outdoors": [
        {"title": "Camping Tent", "price": "$129.99", "link": "https://amazon.com/dp/tent"},
        {"title": "Hiking Backpack", "price": "$99.99", "link": "https://amazon.com/dp/backpack"},
        {"title": "Sleeping Bag", "price": "$79.99", "link": "https://amazon.com/dp/sleepingbag"},
    ],
    "beauty": [
        {"title": "Moisturizer", "price": "$25.99", "link": "https://amazon.com/dp/moisturizer"},
        {"title": "Lipstick", "price": "$15.99", "link": "https://amazon.com/dp/lipstick"},
        {"title": "Eyeliner", "price": "$12.99", "link": "https://amazon.com/dp/eyeliner"},
    ],
}

# === Generate blog posts ===
for category in categories:
    slug = category["slug"]
    title = category["title"]
    description = category["description"]
    products = products_map[slug]

    markdown = generate_markdown(products, title)
    html = generate_html(
        products,
        category_title=title,
        category_description=description,
        template_path="templates/post-template.html"
    )

    output_path = f"posts/post-{slug}.html"
    save_blog_files(title, markdown, html, output_path)
    print(f"✅ Generated blog for: {title}")

# === Generate homepage ===
generate_index_html(categories)
print("🎉 All done! Homepage + blogs generated.")
