# fallback_products.py

AFFILIATE_TAG = "mychanneld-20"

def get_fallback_products(category):
    fallback_data = {
        "kitchen": [
            {
                "title": "Vitamix E310 Explorian Blender",
                "price": "$349.95",
                "link": f"https://www.amazon.com/dp/B07V3L5VZV?tag={AFFILIATE_TAG}",
                "description": "High-performance blender with 10 variable speeds and pulse feature."
            },
            {
                "title": "Breville Smart Oven Pro",
                "price": "$279.95",
                "link": f"https://www.amazon.com/dp/B00XBOXVIA?tag={AFFILIATE_TAG}",
                "description": "Convection toaster oven with slow cook and Element IQ technology."
            },
            {
                "title": "All-Clad D3 Stainless Cookware Set",
                "price": "$699.95",
                "link": f"https://www.amazon.com/dp/B005H05SXM?tag={AFFILIATE_TAG}",
                "description": "10-piece set with tri-ply bonded construction for professional performance."
            },
            {
                "title": "Anova Culinary Sous Vide Precision Cooker Pro",
                "price": "$199.00",
                "link": f"https://www.amazon.com/dp/B07T6DJ8K2?tag={AFFILIATE_TAG}",
                "description": "Professional-grade sous vide with precise temperature control."
            },
            {
                "title": "KitchenAid Artisan Series 5-Qt. Stand Mixer",
                "price": "$449.00",
                "link": f"https://www.amazon.com/dp/B00005UP2P?tag={AFFILIATE_TAG}",
                "description": "Iconic stand mixer with 10 speeds and multiple attachments."
            },
            {
                "title": "Ninja Foodi Pressure Cooker & Air Fryer",
                "price": "$229.99",
                "link": f"https://www.amazon.com/dp/B07S85TPLG?tag={AFFILIATE_TAG}",
                "description": "The pressure cooker that crisps with TenderCrisp Technology."
            },
            {
                "title": "Tramontina 12-Piece Tri-Ply Clad Cookware Set",
                "price": "$249.95",
                "link": f"https://www.amazon.com/dp/B009HBKQR0?tag={AFFILIATE_TAG}",
                "description": "Induction-ready, stainless steel set for everyday use."
            },
            {
                "title": "Instant Pot Pro Plus Smart Electric Pressure Cooker",
                "price": "$169.95",
                "link": f"https://www.amazon.com/dp/B096XTVVBG?tag={AFFILIATE_TAG}",
                "description": "WiFi-enabled smart cooker with 10-in-1 functionality."
            },
            {
                "title": "GE Countertop Nugget Ice Maker",
                "price": "$579.00",
                "link": f"https://www.amazon.com/dp/B07YF9SGBW?tag={AFFILIATE_TAG}",
                "description": "Makes chewable nugget ice fast in your kitchen."
            },
            {
                "title": "Zojirushi Induction Heating Pressure Rice Cooker",
                "price": "$439.00",
                "link": f"https://www.amazon.com/dp/B00HYXR7PG?tag={AFFILIATE_TAG}",
                "description": "High-end rice cooker for perfect texture and flavor."
            }
        ],
        "outdoors": [
            {
                "title": "Coleman Skydome Camping Tent with Screen Room",
                "price": "$249.99",
                "link": f"https://www.amazon.com/dp/B08Q3RZFLM?tag={AFFILIATE_TAG}",
                "description": "Spacious tent with bug-free lounging and fast setup."
            },
            {
                "title": "Garmin Instinct 2 Solar Rugged GPS Smartwatch",
                "price": "$349.99",
                "link": f"https://www.amazon.com/dp/B09N3Z3KW2?tag={AFFILIATE_TAG}",
                "description": "Rugged smartwatch with solar charging and GPS."
            },
            {
                "title": "YETI Tundra 65 Cooler",
                "price": "$350.00",
                "link": f"https://www.amazon.com/dp/B001KZ7QII?tag={AFFILIATE_TAG}",
                "description": "Keeps ice for days—perfect for camping or fishing."
            },
            {
                "title": "Osprey Atmos AG 65 Backpack",
                "price": "$340.00",
                "link": f"https://www.amazon.com/dp/B08KTZW9Z9?tag={AFFILIATE_TAG}",
                "description": "Award-winning anti-gravity backpack for serious hikers."
            },
            {
                "title": "MSR Hubba Hubba NX 2-Person Tent",
                "price": "$479.95",
                "link": f"https://www.amazon.com/dp/B00G6Z8E6S?tag={AFFILIATE_TAG}",
                "description": "Lightweight and durable tent for all-weather camping."
            },
            {
                "title": "DeWalt 20V Max Chainsaw Kit",
                "price": "$199.00",
                "link": f"https://www.amazon.com/dp/B073FTGBZY?tag={AFFILIATE_TAG}",
                "description": "Battery-powered chainsaw for trimming and logging."
            },
            {
                "title": "Weber Q3200 Gas Grill",
                "price": "$499.00",
                "link": f"https://www.amazon.com/dp/B00FDOON9C?tag={AFFILIATE_TAG}",
                "description": "Compact yet powerful grill with dual burners and stand."
            },
            {
                "title": "EGO Power+ 21” Mower Kit",
                "price": "$599.00",
                "link": f"https://www.amazon.com/dp/B07L4TSLM7?tag={AFFILIATE_TAG}",
                "description": "Cordless lawn mower with rapid charging and long run-time."
            },
            {
                "title": "Intex Challenger K2 Kayak Set",
                "price": "$129.00",
                "link": f"https://www.amazon.com/dp/B00177J4JS?tag={AFFILIATE_TAG}",
                "description": "2-person inflatable kayak with paddles and pump."
            },
            {
                "title": "Therm-a-Rest MondoKing 3D Self-Inflating Mattress",
                "price": "$209.95",
                "link": f"https://www.amazon.com/dp/B084ZPQCF8?tag={AFFILIATE_TAG}",
                "description": "Ultimate camping comfort with 4-inch foam support."
            }
        ],
        # Add more categories like 'beauty', 'tech', 'home-decor', 'health' similarly...
    }

    return fallback_data.get(category, [])
