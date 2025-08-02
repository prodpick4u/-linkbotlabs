import random

AFFILIATE_TAG = "mychanneld-20"

def with_tag(asin):
    return f"https://www.amazon.com/dp/{asin}/?tag={AFFILIATE_TAG}"

fallback_products = {
    "kitchen": [
        {"title": "Instant Pot Pro Plus", "price": "$169.95", "url": with_tag("B08PQ2KWHS")},
        {"title": "Ninja AF161 Max XL Air Fryer", "price": "$139.99", "url": with_tag("B07S6529ZZ")},
        {"title": "COSORI Pro II Air Fryer", "price": "$129.99", "url": with_tag("B09C8NP2K3")},
        {"title": "KitchenAid Artisan Series 5-Qt. Mixer", "price": "$449.95", "url": with_tag("B00005UP2P")},
        {"title": "Breville Smart Oven Pro", "price": "$279.95", "url": with_tag("B00XBOXVIA")},
        {"title": "Vitamix 5200 Blender", "price": "$479.95", "url": with_tag("B008H4SLV6")},
        {"title": "Cuckoo 10-Cup Rice Cooker", "price": "$164.99", "url": with_tag("B00IOQ5L1Q")},
        {"title": "All-Clad Stainless Steel Cookware Set", "price": "$699.95", "url": with_tag("B00FXP2AOI")},
        {"title": "GE Profile Opal Nugget Ice Maker", "price": "$579.00", "url": with_tag("B0842FSKJ6")},
        {"title": "Anova Culinary Sous Vide Precision Cooker", "price": "$199.00", "url": with_tag("B07C7PW3PC")}
    ],
    "outdoors": [
        {"title": "Coleman Sundome Camping Tent", "price": "$124.99", "url": with_tag("B07GX54QVW")},
        {"title": "Weber Q1200 Liquid Propane Grill", "price": "$259.00", "url": with_tag("B00FDOON9C")},
        {"title": "Garmin Instinct 2X Solar Watch", "price": "$449.99", "url": with_tag("B0BV3KL25M")},
        {"title": "YETI Tundra 45 Cooler", "price": "$325.00", "url": with_tag("B00IYJK7VS")},
        {"title": "MSR Hubba Hubba 2-Person Tent", "price": "$549.95", "url": with_tag("B08QSPFB6J")},
        {"title": "BioLite FirePit+ Smokeless Grill", "price": "$299.95", "url": with_tag("B08GXXNWRJ")},
        {"title": "TETON Sports Scout 3400 Backpack", "price": "$129.99", "url": with_tag("B000F34ZKS")},
        {"title": "ALPS Mountaineering King Kong Chair", "price": "$129.99", "url": with_tag("B001RLQNSY")},
        {"title": "Jetboil Flash Cooking System", "price": "$124.95", "url": with_tag("B00L1F2I54")},
        {"title": "Garmin GPSMAP 66i", "price": "$599.99", "url": with_tag("B07MW14HVW")}
    ],
    "beauty": [
        {"title": "NuFACE Trinity Starter Kit", "price": "$339.00", "url": with_tag("B01B66YH6K")},
        {"title": "PMD Clean Pro RQ", "price": "$179.00", "url": with_tag("B08FBF2KZT")},
        {"title": "Dyson Supersonic Hair Dryer", "price": "$429.00", "url": with_tag("B01FIG1JIM")},
        {"title": "FOREO LUNA 4 Facial Cleansing", "price": "$279.00", "url": with_tag("B09YH5LK1X")},
        {"title": "Solawave 4-in-1 Skincare Wand", "price": "$169.00", "url": with_tag("B09FYHY2P2")},
        {"title": "T3 AireLuxe Hair Dryer", "price": "$199.99", "url": with_tag("B096G9X1N9")},
        {"title": "Sunday Riley Good Genes", "price": "$122.00", "url": with_tag("B00Q27UX26")},
        {"title": "NuFACE Mini+ Starter Kit", "price": "$245.00", "url": with_tag("B0BDGRH8HK")},
        {"title": "Dr. Dennis Gross DRx SpectraLite Mask", "price": "$435.00", "url": with_tag("B0773X8KS9")},
        {"title": "SkinMedica TNS Advanced+ Serum", "price": "$295.00", "url": with_tag("B08CDVPWKR")}
    ],
    "home-decor": [
        {"title": "Dyson Purifier Cool", "price": "$569.99", "url": with_tag("B093CHZD1N")},
        {"title": "iRobot Braava Jet m6", "price": "$449.99", "url": with_tag("B07RL5L79H")},
        {"title": "Philips Hue Smart Bulbs Kit", "price": "$199.99", "url": with_tag("B07N1WW638")},
        {"title": "Levoit Core 600S Air Purifier", "price": "$299.99", "url": with_tag("B09WYSGBYQ")},
        {"title": "Nixplay 10.1\" Smart Frame", "price": "$179.99", "url": with_tag("B08529TZMC")},
        {"title": "Keurig K-Café Smart", "price": "$249.99", "url": with_tag("B09JVG57TX")},
        {"title": "iRobot Roomba i7+", "price": "$799.99", "url": with_tag("B07GNPDMRP")},
        {"title": "Eufy RoboVac X8 Hybrid", "price": "$549.99", "url": with_tag("B09B24ZN14")},
        {"title": "Ember Temperature Control Smart Mug", "price": "$129.99", "url": with_tag("B07KPLR9P5")},
        {"title": "Philips SmartSleep Wake-up Light", "price": "$149.95", "url": with_tag("B0093162RM")}
    ],
    "tech": [
        {"title": "Apple iPad Air M2", "price": "$599.00", "url": with_tag("B0CVGS9D9C")},
        {"title": "Sony WH-1000XM5 Headphones", "price": "$398.00", "url": with_tag("B09XS7JWHH")},
        {"title": "Oculus Quest 2 VR", "price": "$299.00", "url": with_tag("B099VMT8VZ")},
        {"title": "DJI Osmo Pocket 3", "price": "$519.00", "url": with_tag("B0CJHCDH15")},
        {"title": "LG UltraFine 5K Display", "price": "$1,299.99", "url": with_tag("B07DGN6HR3")},
        {"title": "Samsung T7 SSD 2TB", "price": "$139.99", "url": with_tag("B0874XN4D8")},
        {"title": "Elgato Stream Deck MK.2", "price": "$149.99", "url": with_tag("B0973877N3")},
        {"title": "Anker 737 Power Bank", "price": "$159.99", "url": with_tag("B09WQYF23D")},
        {"title": "Apple AirPods Max", "price": "$549.00", "url": with_tag("B08PZHYWJS")},
        {"title": "Logitech MX Keys", "price": "$119.99", "url": with_tag("B07VZF5DS8")}
    ],
    "health": [
        {"title": "Fitbit Charge 6", "price": "$159.95", "url": with_tag("B0CGVGWVVH")},
        {"title": "RENPHO Smart Body Scale", "price": "$129.99", "url": with_tag("B01N1UX8RW")},
        {"title": "Theragun Mini 2.0", "price": "$199.00", "url": with_tag("B09V2LYG1L")},
        {"title": "Pure Enrichment MistAire XL", "price": "$119.99", "url": with_tag("B01N9KOLUX")},
        {"title": "Withings Sleep Tracking Mat", "price": "$129.95", "url": with_tag("B07CVCHV3H")},
        {"title": "Omron Platinum Monitor", "price": "$104.99", "url": with_tag("B07RZBPMS7")},
        {"title": "Beurer Infrared Heat Lamp", "price": "$139.99", "url": with_tag("B003X26TWM")},
        {"title": "Dodow Sleep Aid Device", "price": "$129.00", "url": with_tag("B00WUX6XGW")},
        {"title": "Carex Day-Light Classic Plus", "price": "$159.99", "url": with_tag("B00PC5HUA6")},
        {"title": "iHealth Air Wireless Oximeter", "price": "$129.99", "url": with_tag("B01MRC0K8X")}
    ]
}

def get_fallback_products(category):
    """Return up to 10 fallback products over $100 for a given category."""
    return fallback_products.get(category, [])
