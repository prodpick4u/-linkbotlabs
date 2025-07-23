import os
import requests

def fetch_amazon_top3_from_rapidapi(category="kitchen"):
    url = "https://amazon-online-data-api.p.rapidapi.com/product-search"
    querystring = {
        "country": "US",
        "keyword": category,
        "page": "1"
    }

    headers = {
        "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
        "X-RapidAPI-Host": "amazon-online-data-api.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        data = response.json()
        
        if not data or "products" not in data or not data["products"]:
            print("❌ No products found.")
            return []

        top3 = data["products"][:3]
        result = []
        for item in top3:
            result.append({
                "title": item.get("title"),
                "image": item.get("main_image"),
                "price": item.get("price_str", "N/A"),
                "url": item.get("url"),
            })

        return result
    except Exception as e:
        print(f"❌ RapidAPI fetch failed: {e}")
        return []
