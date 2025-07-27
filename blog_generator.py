import os
import requests

# Apify integration
def run_apify_actor(input_payload):
    actor_id = os.getenv("APIFY_ACTOR_ID", "jm4192gDoX7CHY7IB")
    token = os.getenv("APIFY_TOKEN")
    url = f"https://api.apify.com/v2/actor-tasks/{actor_id}/run-sync-get-dataset-items?token={token}"
    try:
        resp = requests.post(url, json=input_payload, timeout=60)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"❌ Apify API error: {e}")
        return []

# RapidAPI snippet 1 - Amazon Product Search API
def fetch_amazon_product_details(product_id="B07C3QCJSC", country="us"):
    url = f"https://amazon-product-search-api1.p.rapidapi.com/{product_id}?country={country}"
    headers = {
        "x-rapidapi-host": "amazon-product-search-api1.p.rapidapi.com",
        "x-rapidapi-key": os.getenv("RAPIDAPI_KEY")
    }
    try:
        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"❌ Amazon Product Search API error: {e}")
        return {}

# RapidAPI snippet 2 - Real-Time Product Search API
def fetch_products_by_keyword(keyword="best kitchen gadgets", country="us", limit=3):
    url = (
        f"https://real-time-product-search.p.rapidapi.com/search-light-v2"
        f"?q={keyword}&country={country}&language=en&page=1&limit={limit}"
        f"&sort_by=BEST_MATCH&product_condition=ANY&return_filters=false"
    )
    headers = {
        "x-rapidapi-host": "real-time-product-search.p.rapidapi.com",
        "x-rapidapi-key": os.getenv("RAPIDAPI_KEY")
    }
    try:
        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
        return resp.json().get("data", {}).get("products", [])
    except Exception as e:
        print(f"❌ Real-Time Product Search API error: {e}")
        return []
