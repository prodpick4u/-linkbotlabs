import os
import requests

def fetch_amazon_products(category="kitchen"):
    url = "https://real-time-amazon-data.p.rapidapi.com/bestsellers"
    querystring = {"category": category, "country": "US"}

    headers = {
        "x-rapidapi-key": os.getenv("RAPIDAPI_KEY"),
        "x-rapidapi-host": os.getenv("RAPIDAPI_HOST", "real-time-amazon-data.p.rapidapi.com")
    }

    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        print(f"❌ API request failed: {e}")
        return None

if __name__ == "__main__":
    products_data = fetch_amazon_products("kitchen")
    if products_data:
        print("✅ Fetched products:")
        for product in products_data.get("body", [])[:3]:  # top 3 products
            print(f"- {product['product_title']} | Price: {product['product_price']} | URL: {product['product_url']}")
    else:
        print("No data fetched.")
