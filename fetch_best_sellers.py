python fetch_best_sellers.py
import requests

# Your keys here
RAPIDAPI_KEY = "1cd005eae7msh84dc8a952496e8ap11a8c8jsn1d76048c3e91"
AMAZON_TAG = "mychanneld-20"

def fetch_best_sellers(category="beauty", country="us", page=1, limit=3):
    url = "https://realtime-amazon-data.p.rapidapi.com/best-sellers"
    headers = {
        "x-rapidapi-host": "realtime-amazon-data.p.rapidapi.com",
        "x-rapidapi-key": RAPIDAPI_KEY
    }
    params = {
        "category": category,
        "country": country,
        "page": page
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print(f"❌ API error {response.status_code}: {response.text}")
        return []

    data = response.json()
    products = data.get("products", [])

    # Add affiliate tag to each product link
    for product in products:
        if product.get("link"):
            product["link"] += f"?tag={AMAZON_TAG}"

    return products[:limit]


