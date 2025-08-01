# fallback_products.py

AMAZON_TAG = "mychanneld-20"

def get_fallback_products(category):
    fallback_data = {
        "kitchen": [
            {"title": "Instant Pot Duo 7-in-1", "price": "$99.99", "link": f"https://www.amazon.com/dp/B08PQ2KWHS?tag={AMAZON_TAG}", "description": "Multifunctional pressure cooker — cook meals faster and easier."},
            {"title": "Ninja Air Fryer", "price": "$89.00", "link": f"https://www.amazon.com/dp/B07FDJMC9Q?tag={AMAZON_TAG}", "description": "Crispy food with less oil — compact and easy to clean."},
            {"title": "KitchenAid Artisan Mixer", "price": "$429.95", "link": f"https://www.amazon.com/dp/B00005UP2P?tag={AMAZON_TAG}", "description": "Powerful stand mixer with multiple attachments."},
            {"title": "Lodge Cast Iron Skillet", "price": "$19.90", "link": f"https://www.amazon.com/dp/B00006JSUA?tag={AMAZON_TAG}", "description": "Pre-seasoned cast iron skillet for even cooking."},
            {"title": "OXO Good Grips Salad Spinner", "price": "$29.95", "link": f"https://www.amazon.com/dp/B00004OCKR?tag={AMAZON_TAG}", "description": "Dry greens quickly with a soft non-slip knob and brake."},
            {"title": "Breville Smart Oven Pro", "price": "$279.95", "link": f"https://www.amazon.com/dp/B00XBOXVIA?tag={AMAZON_TAG}", "description": "Convection countertop oven with smart element IQ."},
            {"title": "Brita Water Filter Pitcher", "price": "$26.99", "link": f"https://www.amazon.com/dp/B01FXN3E74?tag={AMAZON_TAG}", "description": "Improves taste and reduces chlorine and other contaminants."},
            {"title": "Dash Mini Waffle Maker", "price": "$12.99", "link": f"https://www.amazon.com/dp/B01M9I779L?tag={AMAZON_TAG}", "description": "Compact waffle maker for single servings — heats quickly."},
            {"title": "Hamilton Beach 2-Way Brewer", "price": "$79.99", "link": f"https://www.amazon.com/dp/B00EI7DPS0?tag={AMAZON_TAG}", "description": "Brew a single cup or full pot — programmable and versatile."},
            {"title": "Mueller Ultra Kettle", "price": "$27.97", "link": f"https://www.amazon.com/dp/B07T1CH2C1?tag={AMAZON_TAG}", "description": "Fast boiling electric kettle with auto shut-off and boil-dry protection."}
        ],
        "outdoors": [
            {"title": "Coleman Sundome Tent", "price": "$79.99", "link": f"https://www.amazon.com/dp/B004J2GUOU?tag={AMAZON_TAG}", "description": "Spacious, weatherproof dome tent — ideal for 2-4 campers."},
            {"title": "LifeStraw Personal Water Filter", "price": "$19.95", "link": f"https://www.amazon.com/dp/B006QF3TW4?tag={AMAZON_TAG}", "description": "Lightweight emergency water filter — perfect for hiking."},
            {"title": "Intex Explorer K2 Kayak", "price": "$149.99", "link": f"https://www.amazon.com/dp/B00A7EXF4C?tag={AMAZON_TAG}", "description": "2-person inflatable kayak for lakes and mild rivers."},
            {"title": "Etekcity Camping Lantern", "price": "$26.99", "link": f"https://www.amazon.com/dp/B00XM0YGW8?tag={AMAZON_TAG}", "description": "Ultra bright LED lanterns, battery-powered for emergencies."},
            {"title": "Coleman Portable Camping Chair", "price": "$39.99", "link": f"https://www.amazon.com/dp/B00363WZSS?tag={AMAZON_TAG}", "description": "Durable folding chair with cooler in the armrest."},
            {"title": "Therm-a-Rest Sleeping Pad", "price": "$47.95", "link": f"https://www.amazon.com/dp/B01N7JTOI3?tag={AMAZON_TAG}", "description": "Ultralight self-inflating pad — perfect for backpacking."},
            {"title": "Wise Owl Outfitters Hammock", "price": "$29.95", "link": f"https://www.amazon.com/dp/B01N4B6VY4?tag={AMAZON_TAG}", "description": "Compact, lightweight hammock with tree straps included."},
            {"title": "Foxelli Trekking Poles", "price": "$59.97", "link": f"https://www.amazon.com/dp/B01L2HYPNW?tag={AMAZON_TAG}", "description": "Collapsible, shock-absorbing poles with adjustable length."},
            {"title": "Coleman Propane Camping Stove", "price": "$57.99", "link": f"https://www.amazon.com/dp/B0009PUR5E?tag={AMAZON_TAG}", "description": "Two-burner portable stove for outdoor cooking."},
            {"title": "Sawyer Products Mini Water Filtration System", "price": "$24.95", "link": f"https://www.amazon.com/dp/B00FA2RLX2?tag={AMAZON_TAG}", "description": "Removes 99.99999% of all bacteria — great for backpacking."}
        ],
        "beauty": [
            {"title": "CeraVe Hydrating Cleanser", "price": "$14.99", "link": f"https://www.amazon.com/dp/B01MSSDEPK?tag={AMAZON_TAG}", "description": "Gentle face wash with ceramides and hyaluronic acid."},
            {"title": "Maybelline Lash Sensational Mascara", "price": "$8.98", "link": f"https://www.amazon.com/dp/B00PFCT0ZA?tag={AMAZON_TAG}", "description": "Lengthens and volumizes lashes with fan effect."},
            {"title": "Olaplex No.3 Hair Perfector", "price": "$30.00", "link": f"https://www.amazon.com/dp/B00SNM5US4?tag={AMAZON_TAG}", "description": "Strengthens damaged hair and restores shine."},
            {"title": "Revlon One-Step Hair Dryer", "price": "$41.88", "link": f"https://www.amazon.com/dp/B01LSUQSB0?tag={AMAZON_TAG}", "description": "Volumizing hot air brush for salon blowouts at home."},
            {"title": "Neutrogena Hydro Boost Gel Cream", "price": "$18.99", "link": f"https://www.amazon.com/dp/B00NR1YQK4?tag={AMAZON_TAG}", "description": "Hydrates skin with hyaluronic acid and absorbs quickly."},
            {"title": "Essie Nail Polish", "price": "$9.00", "link": f"https://www.amazon.com/dp/B00O1A35PQ?tag={AMAZON_TAG}", "description": "Glossy, chip-resistant color in wide shade range."},
            {"title": "e.l.f. Poreless Putty Primer", "price": "$10.00", "link": f"https://www.amazon.com/dp/B07L4JL8Z5?tag={AMAZON_TAG}", "description": "Smooths skin and helps makeup last longer."},
            {"title": "NYX Matte Setting Spray", "price": "$8.47", "link": f"https://www.amazon.com/dp/B00B4YVU4G?tag={AMAZON_TAG}", "description": "Long-lasting setting spray for a matte finish."},
            {"title": "L'Oréal Paris Magic Root Cover Up", "price": "$9.97", "link": f"https://www.amazon.com/dp/B01M7Z83KD?tag={AMAZON_TAG}", "description": "Temporary gray concealer spray — easy and quick fix."},
            {"title": "Bio-Oil Skincare Oil", "price": "$14.99", "link": f"https://www.amazon.com/dp/B004AI97MA?tag={AMAZON_TAG}", "description": "Improves appearance of scars and stretch marks."}
        ],
        "home-decor": [
            {"title": "Philips Hue White and Color Ambiance Starter Kit", "price": "$179.99", "link": f"https://www.amazon.com/dp/B07L6N1YB8?tag={AMAZON_TAG}", "description": "Smart LED light bulbs with millions of colors, compatible with Alexa and Google Assistant."},
            {"title": "Umbra Trigg Geometric Wall Planter", "price": "$34.99", "link": f"https://www.amazon.com/dp/B01N7MRO7V?tag={AMAZON_TAG}", "description": "Modern geometric hanging planter for succulents and small plants."},
            {"title": "Safavieh Monaco Collection Area Rug", "price": "$149.99", "link": f"https://www.amazon.com/dp/B074D3QQNJ?tag={AMAZON_TAG}", "description": "Soft and durable area rug with classic pattern and color."},
            {"title": "West Elm Mid-Century Coffee Table", "price": "$399.00", "link": f"https://www.amazon.com/dp/B08L8QGVNZ?tag={AMAZON_TAG}", "description": "Stylish and sturdy coffee table with walnut veneer."},
            {"title": "IKEA FADO Table Lamp", "price": "$29.99", "link": f"https://www.amazon.com/dp/B008N02PTI?tag={AMAZON_TAG}", "description": "Round glass lamp with soft ambient lighting."},
            {"title": "Yankee Candle Large Jar", "price": "$24.99", "link": f"https://www.amazon.com/dp/B00HLV1TGI?tag={AMAZON_TAG}", "description": "Long-lasting scented candle for a cozy home atmosphere."},
            {"title": "Slipcovered Armchair", "price": "$249.00", "link": f"https://www.amazon.com/dp/B07VJ5PHSR?tag={AMAZON_TAG}", "description": "Comfortable, easy-to-clean slipcover armchair."},
            {"title": "MALM 6-Drawer Dresser", "price": "$229.99", "link": f"https://www.amazon.com/dp/B073TT2Z4P?tag={AMAZON_TAG}", "description": "Simple, functional dresser with ample storage."},
            {"title": "Keenway Floating Shelves", "price": "$39.99", "link": f"https://www.amazon.com/dp/B07X5JYZ13?tag={AMAZON_TAG}", "description": "Set of two wooden shelves with modern design."},
            {"title": "Etekcity LED String Lights", "price": "$19.99", "link": f"https://www.amazon.com/dp/B07NQTPGYL?tag={AMAZON_TAG}", "description": "Battery operated warm white fairy lights for decoration."}
        ],
        "tech": [
            {"title": "Apple AirPods Pro", "price": "$249.00", "link": f"https://www.amazon.com/dp/B07ZPC9QD4?tag={AMAZON_TAG}", "description": "Active noise cancellation wireless earbuds with transparency mode."},
            {"title": "Samsung T7 Portable SSD 1TB", "price": "$109.99", "link": f"https://www.amazon.com/dp/B0874XNQ3Y?tag={AMAZON_TAG}", "description": "Fast external SSD with USB 3.2 Gen 2 for high-speed data transfer."},
            {"title": "Logitech MX Master 3 Mouse", "price": "$99.99", "link": f"https://www.amazon.com/dp/B07S395RWD?tag={AMAZON_TAG}", "description": "Ergonomic wireless mouse with customizable buttons and long battery life."},
            {"title": "Roku Streaming Stick+", "price": "$49.99", "link": f"https://www.amazon.com/dp/B075XLWML4?tag={AMAZON_TAG}", "description": "4K streaming device with voice remote and easy setup."},
            {"title": "Anker PowerCore Portable Charger", "price": "$39.99", "link": f"https://www.amazon.com/dp/B07HBTY5Z2?tag={AMAZON_TAG}", "description": "High capacity power bank with fast charging technology."},
            {"title": "Fitbit Versa 3 Smartwatch", "price": "$229.95", "link": f"https://www.amazon.com/dp/B08DFGPTSK?tag={AMAZON_TAG}", "description": "Health and fitness smartwatch with GPS and heart rate."},
            {"title": "Logitech C920 Webcam", "price": "$69.99", "link": f"https://www.amazon.com/dp/B006JH8T3S?tag={AMAZON_TAG}", "description": "HD 1080p webcam with autofocus and stereo mic."},
            {"title": "Google Nest Mini", "price": "$49.00", "link": f"https://www.amazon.com/dp/B07N8V5Z1N?tag={AMAZON_TAG}", "description": "Smart speaker with Google Assistant for hands-free help."},
            {"title": "Kindle Paperwhite", "price": "$129.99", "link": f"https://www.amazon.com/dp/B07CXG6C9W?tag={AMAZON_TAG}", "description": "Waterproof e-reader with a high-resolution display."},
            {"title": "JBL Flip 5 Bluetooth Speaker", "price": "$99.95", "link": f"https://www.amazon.com/dp/B07QK2SPP7?tag={AMAZON_TAG}", "description": "Portable waterproof speaker with powerful sound."}
        ],
        "health": [
            {"title": "Fitbit Charge 5", "price": "$149.95", "link": f"https://www.amazon.com/dp/B09BXQG2KT?tag={AMAZON_TAG}", "description": "Advanced fitness tracker with heart rate and sleep monitoring."},
            {"title": "Theragun Mini", "price": "$199.00", "link": f"https://www.amazon.com/dp/B07WRKXQWJ?tag={AMAZON_TAG}", "description": "Compact percussive therapy device for muscle relief and recovery."},
            {"title": "Philips Sonicare ProtectiveClean 6100", "price": "$99.95", "link": f"https://www.amazon.com/dp/B07GJ6ZMTT?tag={AMAZON_TAG}", "description": "Electric toothbrush with pressure sensor and multiple cleaning modes."},
            {"title": "Omron Platinum Blood Pressure Monitor", "price": "$69.99", "link": f"https://www.amazon.com/dp/B07RWK3V7V?tag={AMAZON_TAG}", "description": "Clinically accurate home blood pressure monitor."},
            {"title": "Nature Made Vitamin D3", "price": "$12.99", "link": f"https://www.amazon.com/dp/B00LJP3V7U?tag={AMAZON_TAG}", "description": "Supports bone, teeth, muscle, and immune health."},
            {"title": "Gaiam Yoga Mat", "price": "$24.98", "link": f"https://www.amazon.com/dp/B000BQO6V4?tag={AMAZON_TAG}", "description": "Non-slip, thick yoga mat for all fitness levels."},
            {"title": "Waterpik Aquarius Water Flosser", "price": "$79.99", "link": f"https://www.amazon.com/dp/B01CZ0E4T2?tag={AMAZON_TAG}", "description": "Dental water jet for effective plaque removal."},
            {"title": "Dr. Scholl's Orthotic Inserts", "price": "$29.95", "link": f"https://www.amazon.com/dp/B00006I5JU?tag={AMAZON_TAG}", "description": "Comfortable shoe inserts for arch support."},
            {"title": "Bose Sleepbuds II", "price": "$249.00", "link": f"https://www.amazon.com/dp/B07Q9MJKBV?tag={AMAZON_TAG}", "description": "Noise-masking sleepbuds with soothing sounds."},
            {"title": "Pure Enrichment PureGlow Crystal", "price": "$39.99", "link": f"https://www.amazon.com/dp/B07D37FKGY?tag={AMAZON_TAG}", "description": "Himalayan salt lamp for calming ambiance and air purification."}
        ]
    }
    return fallback_data.get(category, [])
