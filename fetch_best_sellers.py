import requests
import os
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "your_default_key")
AMAZON_TAG = os.getenv("AMAZON_TAG", "mychanneld-20")

def add_affiliate_tag(url, tag):
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    query['tag'] = tag
    new_query = urlencode(query, doseq=True)
    return urlunparse(parsed._replace(query=new_query))

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

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        products = data.get("products", [])

        valid_products = []
        for product in products:
            link = product.get("link", "")
            # Check link validity: must include /dp/ and ASIN is 10 chars
            if "/dp/" in link:
                # Extract ASIN from link
                try:
                    asin = link.split("/dp/")[1].split("/")[0]
                    if len(asin) == 10:
                        # Add affiliate tag properly
                        product["link"] = add_affiliate_tag(link, AMAZON_TAG)
                        valid_products.append(product)
                except IndexError:
                    # malformed link, skip product
                    continue
            else:
                # no /dp/ in link, skip product
                continue

        return valid_products[:limit]

    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return []

if __name__ == "__main__":
    print("🔍 Fetching top 3 best sellers in Beauty...\n")
    products = fetch_best_sellers()

    if not products:
        print("❌ No products fetched.")
    else:
        for i, product in enumerate(products, 1):
            print(f"{i}. {product.get('title')}")
            print(f"   Link: {product.get('link')}")
            print(f"   Description: {product.get('description', 'No description available.')}\n")
