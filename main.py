import os
from blog_generator import generate_markdown, generate_html, save_blog_files, generate_index_html

categories = [
    {"title": "Kitchen", "folder": "kitchen"},
    {"title": "Outdoors", "folder": "outdoors"},
    {"title": "Beauty", "folder": "beauty"},
]

# Example product lists - replace with your real data fetching
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

# Ensure category folders exist
for category in categories:
    folder = category["folder"]
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"📁 Created folder: {folder}")

# Generate markdown and HTML posts per category
for category in categories:
    cat_key = category["folder"]
    md = generate_markdown(products_map[cat_key], category["title"])
    template_file = f"templates/post-{cat_key}-template.html"
    html = generate_html(products_map[cat_key], category["title"], template_file)

    output_html_path = f"posts/post-{cat_key}.html"  # Save inside posts/
    save_blog_files(category["title"], md, html, output_html_path)

# Generate the index.html page
generate_index_html(categories, "templates/index-template.html", "index.html")
print("🎉 All done!")
