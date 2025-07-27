import os
import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

AFFILIATE_TAG = "mychanneld-20"

def add_affiliate_tag(url):
    """Append or update the affiliate tag in the Amazon URL."""
    if "amazon." not in url:
        return url  # Not an Amazon link

    parsed = urlparse(url)
    query = parse_qs(parsed.query)

    # Replace or add tag param
    query['tag'] = [AFFILIATE_TAG]

    new_query = urlencode(query, doseq=True)
    new_url = urlunparse(parsed._replace(query=new_query))
    return new_url

def fetch_best_sellers(category="kitchen", limit=3):
    api_key = os.getenv("RAPIDAPI_KEY")
    if not api_key:
        print("❌ RAPIDAPI_KEY not set in environment.")
        return []

    url = "https://real-time-amazon-data.p.rapidapi.com/search"
    querystring = {
        "query": category,
        "page": "1",
        "country": "US"
    }

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "real-time-amazon-data.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        data = response.json()
        items = data.get("data", {}).get("products", [])

        products = []
        for item in items[:limit]:
            title = item.get("title")
            link = add_affiliate_tag(item.get("product_url", ""))
            price = item.get("price_str") or "N/A"
            image = item.get("image_url") or ""
            description = item.get("description") or ""

            if title and link:
                products.append({
                    "title": title.strip(),
                    "link": link,
                    "price": price,
                    "image": image,
                    "description": description
                })

        return products

    except Exception as e:
        print(f"❌ Error fetching products: {e}")
        return []
