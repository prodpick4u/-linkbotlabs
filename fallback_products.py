import random

AFFILIATE_TAG = "mychanneld-20"
FALLBACK_PRODUCTS = {
    "kitchen": [
        {"title":"Breville Barista Express Espresso Machine","price":"$749.95",
         "url":f"https://www.amazon.com/dp/B00CH9QWOU?tag={AFFILIATE_TAG}",
         "description":"Built-in grinder & steam wand for café‑style espresso."},
        {"title":"KitchenAid Artisan 5‑Qt Stand Mixer","price":"$379.99",
         "url":f"https://www.amazon.com/dp/B00005UP2P?tag={AFFILIATE_TAG}",
         "description":"Versatile stand mixer with multiple attachments."},
        {"title":"Vitamix 5200 Blender","price":"$449.95",
         "url":f"https://www.amazon.com/dp/B008H3XZ6Y?tag={AFFILIATE_TAG}",
         "description":"High‑performance variable‑speed blender."},
    ],
    "outdoors": [
        {"title":"Coleman Sundome 4‑Person Tent","price":"$149.99",
         "url":f"https://www.amazon.com/dp/B004J2GUOU?tag={AFFILIATE_TAG}",
         "description":"Weather‑resistant, easy‑setup family tent."},
        {"title":"YETI Tundra 45 Cooler","price":"$299.99",
         "url":f"https://www.amazon.com/dp/B073V7QJDY?tag={AFFILIATE_TAG}",
         "description":"Durable cooler with excellent ice retention."},
        {"title":"Garmin GPSMAP 66i Handheld GPS","price":"$599.99",
         "url":f"https://www.amazon.com/dp/B07RP3FJY4?tag={AFFILIATE_TAG}",
         "description":"InReach communication and navigation device."},
    ],
    "home-decor": [
        {"title":"Dyson Purifier Cool TP07 Fan","price":"$599.99",
         "url":f"https://www.amazon.com/dp/B0949GV3TJ?tag={AFFILIATE_TAG}",
         "description":"Smart HEPA air purifier and cooling fan."},
        {"title":"Philips Hue Color Starter Kit","price":"$199.97",
         "url":f"https://www.amazon.com/dp/B07351P1JK?tag={AFFILIATE_TAG}",
         "description":"Smart bulb kit with 16M colors & voice control."},
        {"title":"iRobot Roomba i3+ Robot Vacuum","price":"$399.99",
         "url":f"https://www.amazon.com/dp/B07GNPDMRP?tag={AFFILIATE_TAG}",
         "description":"Self‑emptying smart robot vacuum."},
    ],
    "beauty": [
        {"title":"Dyson Supersonic Hair Dryer","price":"$429.00",
         "url":f"https://www.amazon.com/dp/B01MQ0M3SO?tag={AFFILIATE_TAG}",
         "description":"Fast‑drying tool with heat control."},
        {"title":"Foreo Luna 4 Cleansing Brush","price":"$279.00",
         "url":f"https://www.amazon.com/dp/B09WJ1TZ34?tag={AFFILIATE_TAG}",
         "description":"T‑Sonic facial cleansing with anti‑aging mode."},
        {"title":"NuFACE Trinity Facial Toning Device","price":"$325.00",
         "url":f"https://www.amazon.com/dp/B01N0QFVWY?tag={AFFILIATE_TAG}",
         "description":"Micro‑current device for facial contouring."},
    ],
    "tech": [
        {"title":"Sony WH‑1000XM5 Headphones","price":"$398.00",
         "url":f"https://www.amazon.com/dp/B09XS7K6WY?tag={AFFILIATE_TAG}",
         "description":"Industry‑leading noise cancellation."},
        {"title":"Apple Watch Series 9 (45 mm)","price":"$429.00",
         "url":f"https://www.amazon.com/dp/B0CHX2F5SP?tag={AFFILIATE_TAG}",
         "description":"Advanced GPS health & fitness tracking."},
        {"title":"Dell UltraSharp 4K 27\" Monitor","price":"$649.99",
         "url":f"https://www.amazon.com/dp/B0B9GYG7D1?tag={AFFILIATE_TAG}",
         "description":"High‑resolution color‑accurate display."},
    ],
    "health": [
        {"title":"Omron Platinum BP Monitor","price":"$109.99",
         "url":f"https://www.amazon.com/dp/B07RL8Z3ZG?tag={AFFILIATE_TAG}",
         "description":"Clinically accurate pressure readings."},
        {"title":"Theragun Elite Percussion Device","price":"$399.00",
         "url":f"https://www.amazon.com/dp/B07N8YGR7R?tag={AFFILIATE_TAG}",
         "description":"Deep tissue muscle recovery tool."},
        {"title":"Philips Sonicare DiamondClean Smart","price":"$199.95",
         "url":f"https://www.amazon.com/dp/B07RFX7QY7?tag={AFFILIATE_TAG}",
         "description":"Smart toothbrush with sensor feedback."},
    ]
}

def get_fallback_products(category, count=3):
    category = category.lower()
    products = FALLBACK_PRODUCTS.get(category, [])
    return random.sample(products, min(count, len(products)))
