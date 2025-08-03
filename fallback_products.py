import random

AFFILIATE_TAG = "mychanneld-20"

FALLBACK_PRODUCTS = {
    "home-decor": [
        {
            "title": "Dyson Purifier Cool™ TP07 Smart Air Purifier",
            "price": "$599.99",
            "url": f"https://www.amazon.com/dp/B0949GV3TJ?tag={AFFILIATE_TAG}",
            "description": "Smart air purifier and fan combo with HEPA filtration and app control, perfect for modern homes."
        },
        {
            "title": "LEVOIT Smart Humidifier with Aroma Diffuser",
            "price": "$109.99",
            "url": f"https://www.amazon.com/dp/B08Q3LS1GQ?tag={AFFILIATE_TAG}",
            "description": "Stylish ultrasonic humidifier with voice control and essential oil tray for a cozy atmosphere."
        },
        {
            "title": "Vornado Whole Room Air Circulator Fan",
            "price": "$129.99",
            "url": f"https://www.amazon.com/dp/B000E5WAUO?tag={AFFILIATE_TAG}",
            "description": "Iconic vortex technology for full-room circulation and quiet performance."
        }
    ],
    "kitchen": [
        {
            "title": "Ninja Foodi 10-in-1 XL Pro Air Fry Oven",
            "price": "$219.99",
            "url": f"https://www.amazon.com/dp/B08GC6PL3D?tag={AFFILIATE_TAG}",
            "description": "All-in-one countertop appliance that air fries, roasts, bakes, and more."
        },
        {
            "title": "Breville Barista Express Espresso Machine",
            "price": "$749.95",
            "url": f"https://www.amazon.com/dp/B00CH9QWOU?tag={AFFILIATE_TAG}",
            "description": "Built-in grinder and steam wand for café-style espresso at home."
        },
        {
            "title": "Vitamix 5200 Blender Professional-Grade",
            "price": "$449.95",
            "url": f"https://www.amazon.com/dp/B001VMAYAM?tag={AFFILIATE_TAG}",
            "description": "High-performance blender with variable speed control and stainless steel blades."
        }
    ],
    "outdoors": [
        {
            "title": "Coleman Skydome Camping Tent",
            "price": "$149.99",
            "url": f"https://www.amazon.com/dp/B08L6YJ5ZK?tag={AFFILIATE_TAG}",
            "description": "Easy 5-minute setup tent with dark room technology and weather protection."
        },
        {
            "title": "Weber Q1200 Liquid Propane Grill",
            "price": "$259.00",
            "url": f"https://www.amazon.com/dp/B00FDOON9C?tag={AFFILIATE_TAG}",
            "description": "Compact yet powerful gas grill for backyard or travel use."
        },
        {
            "title": "Solo Stove Bonfire 2.0",
            "price": "$299.99",
            "url": f"https://www.amazon.com/dp/B0B2D7MT4R?tag={AFFILIATE_TAG}",
            "description": "Smokeless stainless steel fire pit perfect for outdoor gatherings."
        }
    ],
    "beauty": [
        {
            "title": "Dyson Supersonic Hair Dryer",
            "price": "$429.00",
            "url": f"https://www.amazon.com/dp/B01MQ0M3SO?tag={AFFILIATE_TAG}",
            "description": "Fast-drying hair care tool with intelligent heat control and magnetic attachments."
        },
        {
            "title": "PMD Clean Pro RQ Smart Facial Cleansing Device",
            "price": "$179.00",
            "url": f"https://www.amazon.com/dp/B07X6LZ9ZG?tag={AFFILIATE_TAG}",
            "description": "SonicGlow technology and rose quartz facial massager for deep cleansing and anti-aging."
        },
        {
            "title": "Foreo Luna 4 Facial Cleansing Brush",
            "price": "$279.00",
            "url": f"https://www.amazon.com/dp/B09WJ1TZ34?tag={AFFILIATE_TAG}",
            "description": "Advanced T-Sonic device with personalized skincare modes."
        }
    ],
    "tech": [
        {
            "title": "Apple Watch Series 9 (GPS, 45mm)",
            "price": "$429.00",
            "url": f"https://www.amazon.com/dp/B0CHX2F5SP?tag={AFFILIATE_TAG}",
            "description": "Track your health, fitness, and productivity with the latest Apple Watch."
        },
        {
            "title": "Logitech MX Keys S Wireless Keyboard",
            "price": "$109.99",
            "url": f"https://www.amazon.com/dp/B0C5C9KZ65?tag={AFFILIATE_TAG}",
            "description": "Smart illumination and quiet typing with multi-device support."
        },
        {
            "title": "Samsung Galaxy Buds2 Pro",
            "price": "$229.99",
            "url": f"https://www.amazon.com/dp/B0B6FDM5QN?tag={AFFILIATE_TAG}",
            "description": "True wireless noise-canceling earbuds with immersive sound and comfort."
        }
    ],
    "health": [
        {
            "title": "Omron Platinum Blood Pressure Monitor",
            "price": "$109.99",
            "url": f"https://www.amazon.com/dp/B07RL8Z3ZG?tag={AFFILIATE_TAG}",
            "description": "Clinically accurate readings with Bluetooth sync and dual-user support."
        },
        {
            "title": "RENPHO Smart Scale for Body Weight",
            "price": "$139.99",
            "url": f"https://www.amazon.com/dp/B07Y2XQ4Z4?tag={AFFILIATE_TAG}",
            "description": "Tracks 13 body metrics and syncs with fitness apps."
        },
        {
            "title": "Fitbit Charge 6 Fitness Tracker",
            "price": "$159.95",
            "url": f"https://www.amazon.com/dp/B0C6J79PTF?tag={AFFILIATE_TAG}",
            "description": "Monitor heart rate, sleep, GPS activity, and stress with Google integration."
        }
    ]
}

AFFILIATE_DISCLAIMER = """
<p style="font-size:0.9rem; color:#999; margin-top:1rem;">
  As an Amazon Associate I earn from qualifying purchases.
</p>
"""

def get_fallback_products(category, count=3):
    """
    Returns up to `count` randomly selected fallback products from the given category.
    If category not found, returns empty list.
    """
    products = FALLBACK_PRODUCTS.get(category, [])
    if not products:
        return []
    return random.sample(products, min(count, len(products)))
