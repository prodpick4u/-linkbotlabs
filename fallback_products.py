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
        },
        {
            "title": "Philips Hue White and Color Ambiance Starter Kit",
            "price": "$199.99",
            "url": f"https://www.amazon.com/dp/B07351P1JK?tag={AFFILIATE_TAG}",
            "description": "Smart lighting kit with customizable colors and voice control."
        },
        {
            "title": "Nespresso Vertuo Coffee and Espresso Machine",
            "price": "$159.00",
            "url": f"https://www.amazon.com/dp/B01MYRR6XO?tag={AFFILIATE_TAG}",
            "description": "Easy-to-use coffee maker with barcode brewing technology."
        },
        {
            "title": "iRobot Roomba i3+ (3550) Robot Vacuum",
            "price": "$399.99",
            "url": f"https://www.amazon.com/dp/B07GNPDMRP?tag={AFFILIATE_TAG}",
            "description": "Smart robot vacuum with automatic dirt disposal."
        },
        {
            "title": "Sonos One (Gen 2) - Voice Controlled Smart Speaker",
            "price": "$199.00",
            "url": f"https://www.amazon.com/dp/B07W95BQ69?tag={AFFILIATE_TAG}",
            "description": "Rich sound with Alexa and Google Assistant built-in."
        },
        {
            "title": "Levoit Air Purifier for Home",
            "price": "$139.99",
            "url": f"https://www.amazon.com/dp/B07VVK39F7?tag={AFFILIATE_TAG}",
            "description": "Compact air purifier with HEPA filter for allergens and dust."
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
        },
        {
            "title": "Instant Pot Duo Evo Plus Pressure Cooker",
            "price": "$159.99",
            "url": f"https://www.amazon.com/dp/B07RCNHTLS?tag={AFFILIATE_TAG}",
            "description": "7-in-1 multicooker for fast, easy cooking."
        },
        {
            "title": "All-Clad Stainless Steel Cookware Set, 10-Piece",
            "price": "$599.95",
            "url": f"https://www.amazon.com/dp/B004T6MSIS?tag={AFFILIATE_TAG}",
            "description": "Professional-grade cookware with superior heat conduction."
        },
        {
            "title": "Cuisinart 14-Cup Food Processor",
            "price": "$199.95",
            "url": f"https://www.amazon.com/dp/B01AXM4WVY?tag={AFFILIATE_TAG}",
            "description": "Powerful food processor for chopping, slicing, and shredding."
        },
        {
            "title": "KitchenAid Artisan Series 5-Qt Stand Mixer",
            "price": "$379.99",
            "url": f"https://www.amazon.com/dp/B00005UP2P?tag={AFFILIATE_TAG}",
            "description": "Versatile mixer with multiple attachments."
        },
        {
            "title": "Breville Smart Oven Air Fryer",
            "price": "$399.95",
            "url": f"https://www.amazon.com/dp/B07WTH7B8N?tag={AFFILIATE_TAG}",
            "description": "Convection oven with air fry and dehydrate functions."
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
        },
        {
            "title": "Garmin GPSMAP 66i Handheld Hiking GPS",
            "price": "$599.99",
            "url": f"https://www.amazon.com/dp/B07RR5KWMC?tag={AFFILIATE_TAG}",
            "description": "Satellite communication and navigation device."
        },
        {
            "title": "Therm-a-Rest NeoAir XTherm Sleeping Pad",
            "price": "$199.95",
            "url": f"https://www.amazon.com/dp/B06W55JYD7?tag={AFFILIATE_TAG}",
            "description": "Lightweight and warm sleeping pad for camping."
        },
        {
            "title": "YETI Rambler 36 oz Tumbler",
            "price": "$39.99",
            "url": f"https://www.amazon.com/dp/B01J5EOM68?tag={AFFILIATE_TAG}",
            "description": "Durable insulated tumbler for hot or cold drinks."
        },
        {
            "title": "Osprey Atmos AG 65 Backpack",
            "price": "$269.99",
            "url": f"https://www.amazon.com/dp/B07TJRGWYQ?tag={AFFILIATE_TAG}",
            "description": "High-performance hiking backpack with anti-gravity suspension."
        },
        {
            "title": "Black Diamond Spot Headlamp",
            "price": "$39.95",
            "url": f"https://www.amazon.com/dp/B00NHHY4IS?tag={AFFILIATE_TAG}",
            "description": "Powerful and waterproof headlamp for outdoor adventures."
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
        },
        {
            "title": "Revlon One-Step Hair Dryer & Volumizer",
            "price": "$139.99",
            "url": f"https://www.amazon.com/dp/B07Q3FYK5L?tag={AFFILIATE_TAG}",
            "description": "Dryer and volumizer combo for silky smooth hair."
        },
        {
            "title": "Olaplex Hair Perfector No 3 Repairing Treatment",
            "price": "$28.00",
            "url": f"https://www.amazon.com/dp/B00SNM5US4?tag={AFFILIATE_TAG}",
            "description": "Hair treatment to repair damaged and broken hair."
        },
        {
            "title": "Clarisonic Mia Smart Facial Cleansing Brush",
            "price": "$149.00",
            "url": f"https://www.amazon.com/dp/B01N0U7YKM?tag={AFFILIATE_TAG}",
            "description": "Personalized skincare with smart technology."
        },
        {
            "title": "NuFACE Trinity Facial Toning Device",
            "price": "$325.00",
            "url": f"https://www.amazon.com/dp/B01N0QFVWY?tag={AFFILIATE_TAG}",
            "description": "Microcurrent device for facial contouring and wrinkle reduction."
        },
        {
            "title": "T3 Cura Luxe Hair Dryer",
            "price": "$299.00",
            "url": f"https://www.amazon.com/dp/B00I58L0KS?tag={AFFILIATE_TAG}",
            "description": "Professional hair dryer with ionic technology."
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
        },
        {
            "title": "Sony WH-1000XM5 Wireless Noise-Canceling Headphones",
            "price": "$398.00",
            "url": f"https://www.amazon.com/dp/B09XS7K6WY?tag={AFFILIATE_TAG}",
            "description": "Industry-leading noise cancellation and premium sound quality."
        },
        {
            "title": "Kindle Paperwhite (11th Gen)",
            "price": "$139.99",
            "url": f"https://www.amazon.com/dp/B08N36XNTT?tag={AFFILIATE_TAG}",
            "description": "Waterproof e-reader with adjustable warm light."
        },
        {
            "title": "Anker PowerCore 26800 Portable Charger",
            "price": "$99.99",
            "url": f"https://www.amazon.com/dp/B01N0X3NL5?tag={AFFILIATE_TAG}",
            "description": "High-capacity portable power bank with fast charging."
        },
        {
            "title": "Dell UltraSharp U2723QE 27-inch 4K Monitor",
            "price": "$649.99",
            "url": f"https://www.amazon.com/dp/B0B9GYG7D1?tag={AFFILIATE_TAG}",
            "description": "Ultra-clear 4K resolution with wide color gamut."
        },
        {
            "title": "Logitech StreamCam Full HD Webcam",
            "price": "$169.99",
            "url": f"https://www.amazon.com/dp/B07K95WFWM?tag={AFFILIATE_TAG}",
            "description": "Perfect for streaming and video conferencing."
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
        },
        {
            "title": "Withings Body+ - Smart Body Composition Wi-Fi Scale",
            "price": "$99.95",
            "url": f"https://www.amazon.com/dp/B074VFY3QD?tag={AFFILIATE_TAG}",
            "description": "Advanced weight and body composition tracking."
        },
        {
            "title": "Theragun Elite Handheld Percussive Therapy Device",
            "price": "$399.00",
            "url": f"https://www.amazon.com/dp/B07N8YGR7R?tag={AFFILIATE_TAG}",
            "description": "Muscle treatment device for deep tissue massage."
        },
        {
            "title": "Philips Sonicare DiamondClean Smart 9750",
            "price": "$199.95",
            "url": f"https://www.amazon.com/dp/B07RFX7QY7?tag={AFFILIATE_TAG}",
            "description": "Electric toothbrush with smart sensor technology."
        },
        {
            "title": "Hydro Flask Standard Mouth Water Bottle",
            "price": "$39.95",
            "url": f"https://www.amazon.com/dp/B01ACAX6Q0?tag={AFFILIATE_TAG}",
            "description": "Durable insulated water bottle keeps drinks cold or hot."
        },
        {
            "title": "Garmin Forerunner 245 Music GPS Running Watch",
            "price": "$299.99",
            "url": f"https://www.amazon.com/dp/B07Q29X3YK?tag={AFFILIATE_TAG}",
            "description": "GPS running watch with advanced training features."
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
