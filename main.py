import os
import requests

def fetch_best_sellers():
    url = "https://realtime-amazon-data.p.rapidapi.com/best-sellers"
    headers = {
        "x-rapidapi-host": "realtime-amazon-data.p.rapidapi.com",
        "x-rapidapi-key": os.getenv("RAPIDAPI_KEY")
    }
    params = {
        "category": "mobile-apps",
        "country": "us",
        "page": 1
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print(f"API error {response.status_code}: {response.text}")
        return []

    data = response.json()
    products = data.get("products", [])
    return products

if __name__ == "__main__":
    products = fetch_best_sellers()
    if not products:
        print("No products fetched.")
    else:
        for i, product in enumerate(products[:3], 1):
            print(f"{i}. {product.get('title')}")
            print(f"   Link: {product.get('link')}")
            print(f"   Description: {product.get('description', 'No description')}\n")
