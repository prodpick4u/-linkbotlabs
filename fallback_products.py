AMAZON_TAG = "mychanneld-20"

def get_fallback_products(category):
    fallback_data = {
        "kitchen": [
            {
                "title": "Instant Pot Duo 7-in-1",
                "price": "$99.99",
                "link": f"https://www.amazon.com/dp/B08PQ2KWHS?tag={AMAZON_TAG}",
                "description": "Multifunctional pressure cooker — cook meals faster and easier."
            },
            {
                "title": "Ninja Air Fryer",
                "price": "$89.00",
                "link": f"https://www.amazon.com/dp/B07FDJMC9Q?tag={AMAZON_TAG}",
                "description": "Crispy food with less oil — compact and easy to clean."
            },
            {
                "title": "KitchenAid Artisan Mixer",
                "price": "$429.95",
                "link": f"https://www.amazon.com/dp/B00005UP2P?tag={AMAZON_TAG}",
                "description": "Powerful stand mixer with multiple attachments."
            },
        ],
        "outdoors": [
            {
                "title": "Coleman Sundome Tent",
                "price": "$79.99",
                "link": f"https://www.amazon.com/dp/B004J2GUOU?tag={AMAZON_TAG}",
                "description": "Spacious, weatherproof dome tent — ideal for 2-4 campers."
            },
            {
                "title": "LifeStraw Personal Water Filter",
                "price": "$19.95",
                "link": f"https://www.amazon.com/dp/B006QF3TW4?tag={AMAZON_TAG}",
                "description": "Lightweight emergency water filter — perfect for hiking."
            },
            {
                "title": "Intex Explorer K2 Kayak",
                "price": "$149.99",
                "link": f"https://www.amazon.com/dp/B00A7EXF4C?tag={AMAZON_TAG}",
                "description": "2-person inflatable kayak for lakes and mild rivers."
            },
        ],
        "beauty": [
            {
                "title": "CeraVe Hydrating Cleanser",
                "price": "$14.99",
                "link": f"https://www.amazon.com/dp/B01MSSDEPK?tag={AMAZON_TAG}",
                "description": "Gentle face wash with ceramides and hyaluronic acid."
            },
            {
                "title": "Maybelline Lash Sensational Mascara",
                "price": "$8.98",
                "link": f"https://www.amazon.com/dp/B00PFCT0ZA?tag={AMAZON_TAG}",
                "description": "Lengthens and volumizes lashes with fan effect."
            },
            {
                "title": "Olaplex No.3 Hair Perfector",
                "price": "$30.00",
                "link": f"https://www.amazon.com/dp/B00SNM5US4?tag={AMAZON_TAG}",
                "description": "Strengthens damaged hair and restores shine."
            },
        ],
        "household": [
            {
                "title": "iRobot Roomba i3+ EVO Self-Emptying Robot Vacuum",
                "price": "$399.99",
                "link": f"https://www.amazon.com/dp/B09NQNG7QJ?tag={AMAZON_TAG}",
                "description": "Self-emptying smart vacuum with powerful suction — perfect for pet-friendly homes."
            },
            {
                "title": "Levoit Core 300S Smart Air Purifier",
                "price": "$149.99",
                "link": f"https://www.amazon.com/dp/B08WJPBDFC?tag={AMAZON_TAG}",
                "description": "HEPA air filter with app and voice control — removes allergens and odors quietly."
            },
            {
                "title": "Tineco Floor ONE S5 Wet Dry Vacuum Cleaner",
                "price": "$499.00",
                "link": f"https://www.amazon.com/dp/B094N8YF1X?tag={AMAZON_TAG}",
                "description": "2-in-1 mop and vacuum for deep cleaning hard floors with smart sensor technology."
            }
        ],
        "tech": [
            {
                "title": "Apple AirPods Pro",
                "price": "$249.00",
                "link": f"https://www.amazon.com/dp/B07ZPC9QD4?tag={AMAZON_TAG}",
                "description": "Active noise cancellation wireless earbuds with transparency mode."
            },
            {
                "title": "Samsung T7 Portable SSD 1TB",
                "price": "$109.99",
                "link": f"https://www.amazon.com/dp/B0874XNQ3Y?tag={AMAZON_TAG}",
                "description": "Fast external SSD with USB 3.2 Gen 2 for high-speed data transfer."
            },
            {
                "title": "Logitech MX Master 3 Mouse",
                "price": "$99.99",
                "link": f"https://www.amazon.com/dp/B07S395RWD?tag={AMAZON_TAG}",
                "description": "Ergonomic wireless mouse with customizable buttons and long battery life."
            }
        ],
        "health": [
            {
                "title": "Fitbit Charge 5",
                "price": "$149.95",
                "link": f"https://www.amazon.com/dp/B09BXQG2KT?tag={AMAZON_TAG}",
                "description": "Advanced fitness tracker with heart rate and sleep monitoring."
            },
            {
                "title": "Theragun Mini",
                "price": "$199.00",
                "link": f"https://www.amazon.com/dp/B07WRKXQWJ?tag={AMAZON_TAG}",
                "description": "Compact percussive therapy device for muscle relief and recovery."
            },
            {
                "title": "Philips Sonicare ProtectiveClean 6100",
                "price": "$99.95",
                "link": f"https://www.amazon.com/dp/B07GJ6ZMTT?tag={AMAZON_TAG}",
                "description": "Electric toothbrush with pressure sensor and multiple cleaning modes."
            }
        ],
        "home-decor": [
            {
                "title": "Philips Hue White and Color Ambiance Starter Kit",
                "price": "$179.99",
                "link": f"https://www.amazon.com/dp/B07L6N1YB8?tag={AMAZON_TAG}",
                "description": "Smart LED light bulbs with millions of colors, compatible with Alexa and Google Assistant."
            },
            {
                "title": "Umbra Trigg Geometric Wall Planter",
                "price": "$34.99",
                "link": f"https://www.amazon.com/dp/B01N7MRO7V?tag={AMAZON_TAG}",
                "description": "Modern geometric hanging planter for succulents and small plants."
            },
            {
                "title": "Safavieh Monaco Collection Area Rug",
                "price": "$149.99",
                "link": f"https://www.amazon.com/dp/B074D3QQNJ?tag={AMAZON_TAG}",
                "description": "Soft and durable area rug with classic pattern and color."
            }
        ]
    }

    return fallback_data.get(category, [])
