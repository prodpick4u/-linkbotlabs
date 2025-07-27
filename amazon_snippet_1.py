import requests
import os

def fetch_amazon_product_details(product_id="B07C3QCJSC", country="us"):
    url = f"https://amazon-product-search-api1.p.rapidapi.com/{product_id}?country={country}"
    headers = {
        "x-rapidapi-host": "amazon-product-search-api1.p.rapidapi.com",
        "x-rapidapi-key": os.getenv("RAPIDAPI_KEY")
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("❌ Amazon API 1 error:", response.text)
        return {}
