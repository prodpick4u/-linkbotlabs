from fetch_best_sellers import fetch_best_sellers
from blog_generator import generate_post_html, generate_index_html

# Step 1: Fetch top 3 products from Amazon via RapidAPI
kitchen_products = fetch_best_sellers(category="kitchen")
outdoor_products = fetch_best_sellers(category="outdoors")
beauty_products = fetch_best_sellers(category="beauty")

# Step 2: Build category metadata (title, emoji, post template, image, etc.)
categories = [
    {
        "title": "Top Kitchen Gadgets for 2025",
        "emoji": "🥘",
        "description": "Discover the latest and greatest kitchen gadgets that will make your cooking easier and more fun.",
        "post_path": "posts/post-kitchen.html",
        "products": kitchen_products,
        "template": "templates/post-kitchen-template.html",
        "image_url": "https://images.unsplash.com/photo-1607274968450-ccd2f8f60fbe?fit=crop&w=600&q=60"
    },
    {
        "title": "Best Outdoor Gear This Season",
        "emoji": "🏕️",
        "description": "Explore the best outdoor gear to keep you prepared for your next adventure.",
        "post_path": "posts/post-outdoor.html",
        "products": outdoor_products,
        "template": "templates/post-outdoor-template.html",
        "image_url": "https://images.unsplash.com/photo-1606788075761-63f4f3934d5a?fit=crop&w=600&q=60"
    },
    {
        "title": "Must-Have Beauty Products",
        "emoji": "💄",
        "description": "Your skincare and makeup essentials for 2025.",
        "post_path": "posts/post-beauty.html",
        "products": beauty_products,
        "template": "templates/post-beauty-template.html",
        "image_url": "https://images.unsplash.com/photo-1588776814546-f63f4455e0cf?fit=crop&w=600&q=60"
    }
]

# Step 3: Generate blog posts per category
for cat in categories:
    if cat["products"]:
        generate_post_html(cat["products"], cat["template"], cat["post_path"])
    else:
        print(f"⚠️ No products found for {cat['title']} — skipping post generation.")

# Step 4: Generate front page with all category previews
generate_index_html(categories, "templates/index-template.html", "index.html")
