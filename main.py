import os
from blog_generator import generate_markdown, generate_html, save_blog_files, generate_index_html

# Define your categories and folders
categories = [
    {"title": "Kitchen", "folder": "kitchen"},
    {"title": "Outdoors", "folder": "outdoors"},
    {"title": "Beauty", "folder": "beauty"},
]

# Sample product data — replace with your real fetch logic
kitchen_products = [
    {"title": "Knife Set", "price": "$59.99", "link": "https://amazon.com/dp/knife"},
    {"title": "Blender", "price": "$89.99", "link": "https://amazon.com/dp/blender"},
    {"title": "Cutting Board", "price": "$19.99", "link": "https://amazon.com/dp/cuttingboard"},
]

outdoor_products = [
    {"title": "Camping Tent", "price": "$129.99", "link": "https://amazon.com/dp/tent"},
    {"title": "Hiking Backpack", "price": "$99.99", "link": "https://amazon.com/dp/backpack"},
    {"title": "Sleeping Bag", "price": "$79.99", "link": "https://amazon.com/dp/sleepingbag"},
]

beauty_products = [
    {"title": "Moisturizer", "price": "$25.99", "link": "https://amazon.com/dp/moisturizer"},
    {"title": "Lipstick", "price": "$15.99", "link": "https://amazon.com/dp/lipstick"},
    {"title": "Eyeliner", "price": "$12.99", "link": "https://amazon.com/dp/eyeliner"},
]

products_map = {
    "kitchen": kitchen_products,
    "outdoors": outdoor_products,
    "beauty": beauty_products,
}

# Step 1: Ensure all category folders exist
for category in categories:
    folder = category["folder"]
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"📁 Created folder: {folder}")

# Step 2: Generate and save markdown + HTML for each category
for category in categories:
    cat_key = category["folder"]

    md = generate_markdown(products_map[cat_key], category["title"])
    template_file = f"templates/post-{cat_key}-template.html"
    html = generate_html(products_map[cat_key], category["title"], template_file)

    output_html_path = f"{cat_key}/index.html"
    save_blog_files(category["title"], md, html, output_html_path)

# Step 3: Generate main index.html page linking all categories
generate_index_html(categories, "templates/index-template.html", "index.html")
