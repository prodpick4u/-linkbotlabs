import os
from fetch_best_sellers import fetch_best_sellers
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

# === Fallback products ===

fallback_kitchen_products = [
    {
        "title": "Ninja AF101 Air Fryer",
        "price": "$89.99",
        "link": "https://www.amazon.com/dp/B07FDJMC9Q?tag=mychanneld-20",
        "description": "Crisp, roast, reheat, and dehydrate with this 4-quart air fryer.",
        "image": "https://m.media-amazon.com/images/I/71IP8HnKkXL._AC_SL1500_.jpg",
        "video_url": "https://www.youtube.com/embed/SCaQZCpxv2w"
    },
    {
        "title": "Instant Pot Duo 7-in-1",
        "price": "$99.95",
        "link": "https://www.amazon.com/dp/B08PQ2KWHS?tag=mychanneld-20",
        "description": "The multi-cooker that does it all — pressure cook, sauté, steam and more.",
        "image": "https://m.media-amazon.com/images/I/81R2N4R6NEL._AC_SL1500_.jpg",
        "video_url": "https://www.youtube.com/embed/uT0pW-i9blA"
    },
    {
        "title": "COSORI Electric Kettle",
        "price": "$39.99",
        "link": "https://www.amazon.com/dp/B09XY4S8MS?tag=mychanneld-20",
        "description": "Fast boiling glass kettle with auto shut-off and boil-dry protection.",
        "image": "https://m.media-amazon.com/images/I/61rcoU0e5nL._AC_SL1500_.jpg",
        "video_url": "https://www.youtube.com/embed/mqENNKHjgj0"
    }
]

fallback_outdoor_products = [
    {
        "title": "Coleman Sundome Tent",
        "price": "$99.99",
        "link": "https://www.amazon.com/dp/B004J2GUOU?tag=mychanneld-20",
        "description": "A reliable and spacious 4-person tent perfect for camping trips.",
        "image": "https://m.media-amazon.com/images/I/71DbxCpiPPL._AC_SL1500_.jpg",
        "video_url": "https://www.youtube.com/embed/QcXqJ6UOZ9s"
    },
    {
        "title": "LifeStraw Personal Water Filter",
        "price": "$19.95",
        "link": "https://www.amazon.com/dp/B006QF3TW4?tag=mychanneld-20",
        "description": "Essential for safe drinking water during hiking and camping adventures.",
        "image": "https://m.media-amazon.com/images/I/81NdiFkz-ML._AC_SL1500_.jpg",
        "video_url": "https://www.youtube.com/embed/6x4ttgCR7oc"
    },
    {
        "title": "TETON Sports Celsius XXL Sleeping Bag",
        "price": "$79.99",
        "link": "https://www.amazon.com/dp/B000F37PDU?tag=mychanneld-20",
        "description": "A warm, comfortable sleeping bag rated for cold-weather camping.",
        "image": "https://m.media-amazon.com/images/I/81F7lpt7jNL._AC_SL1500_.jpg",
        "video_url": "https://www.youtube.com/embed/sJMuRybqB4o"
    }
]

fallback_beauty_products = [
    {
        "title": "CeraVe Hydrating Facial Cleanser",
        "price": "$14.99",
        "link": "https://www.amazon.com/dp/B01MSSDEPK?tag=mychanneld-20",
        "description": "Gentle face wash with hyaluronic acid and ceramides for normal to dry skin.",
        "image": "https://m.media-amazon.com/images/I/71pvvrT8XwL._SL1500_.jpg",
        "video_url": "https://www.youtube.com/embed/nYCP4-py7uI"
    },
    {
        "title": "Maybelline Lash Sensational Mascara",
        "price": "$8.98",
        "link": "https://www.amazon.com/dp/B00PFCT8J2?tag=mychanneld-20",
        "description": "Define and lengthen lashes with this bestselling drugstore mascara.",
        "image": "https://m.media-amazon.com/images/I/71ZwCVVNO8L._SL1500_.jpg",
        "video_url": "https://www.youtube.com/embed/BGE9VA-8bww"
    },
    {
        "title": "Neutrogena Hydro Boost Water Gel",
        "price": "$16.72",
        "link": "https://www.amazon.com/dp/B00NR1YQK4?tag=mychanneld-20",
        "description": "Lightweight moisturizer with hyaluronic acid for 48-hour hydration.",
        "image": "https://m.media-amazon.com/images/I/61p9Ggfz6nL._SL1500_.jpg",
        "video_url": "https://www.youtube.com/embed/tkKtkUGXgFo"
    }
]

# === Map fallback data ===
fallbacks = {
    "kitchen": fallback_kitchen_products,
    "outdoors": fallback_outdoor_products,
    "beauty": fallback_beauty_products
}

# === Fetch product data or fallback ===
products_map = {}

for category in categories:
    slug = category["slug"]
    print(f"🔍 Fetching products for category: {slug}")
    products = fetch_best_sellers(category=slug, limit=3)

    if not products:
        print(f"⚠️ No products fetched for {slug}. Using fallback.")
        products = fallbacks.get(slug, [])

    products_map[slug] = products

# === Generate blog posts for each category ===
for category in categories:
    slug = category["slug"]
    title = category["title"]
    description = category["description"]
    products = products_map.get(slug, [])

    if not products:
        print(f"⚠️ No products found for {title}, skipping blog generation.")
        continue

    markdown = generate_markdown(products, title)
    html = generate_html(
        products,
        category_title=title,
        category_description=description,
        template_path="posts/post-template.html"
    )

    output_path = f"posts/post-{slug}.html"
    save_blog_files(title, markdown, html, output_path)
    print(f"✅ Generated blog for: {title}")

# === Generate homepage with links to blogs ===
generate_index_html(
    categories,
    template_path="index-template.html",
    output_path="index.html"
)

print("🎉 All done! Homepage and blog posts generated successfully.")
