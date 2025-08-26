import requests
import os

def fetch_products_by_keyword(keyword="Nike shoes", country="us", limit=5):
    url = (
        "https://real-time-product-search.p.rapidapi.com/search-light-v2"
        f"?q={keyword}&country={country}&language=en&page=1&limit={limit}"
        "&sort_by=BEST_MATCH&product_condition=ANY&return_filters=false"
    )
    headers = {
        "x-rapidapi-host": "real-time-product-search.p.rapidapi.com",
        "x-rapidapi-key": os.getenv("RAPIDAPI_KEY")
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("data", {}).get("products", [])
    else:
        print("❌ Rapid Product Search API error:", response.text)
        return []
