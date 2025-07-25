import requests
import os
import time
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode

from fallback_products import get_fallback_products

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "your_default_key")
AMAZON_TAG = os.getenv("AMAZON_TAG", "mychanneld-20")

def add_affiliate_tag(url, tag):
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    query['tag'] = tag
    new_query = urlencode(query, doseq=True)
    return urlunparse(parsed._replace(query=new_query))

def fetch_best_sellers(category="beauty", country="us", page=1, limit=3, max_retries=3):
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

    if RAPIDAPI_KEY == "your_default_key" or not RAPIDAPI_KEY:
        print("⚠️ RAPIDAPI_KEY is not set. Using fallback products.")
        return get_fallback_products(category)

    retry = 0
    wait_time = 2
    total_waited = 0
    MAX_TOTAL_WAIT = 20

    while retry < max_retries and total_waited <= MAX_TOTAL_WAIT:
        try:
            print(f"➡️ Requesting API for category '{category}' (try {retry + 1})...")
            response = requests.get(url, headers=headers, params=params, timeout=15)
            print("✅ Response received")
            response.raise_for_status()

            data = response.json()
            products = data.get("products", [])

            valid_products = []
            for product in products:
                link = product.get("link", "")
                if "/dp/" in link:
                    try:
                        asin = link.split("/dp/")[1].split("/")[0]
                        if len(asin) == 10:
                            product["link"] = add_affiliate_tag(link, AMAZON_TAG)
                            valid_products.append(product)
                    except IndexError:
                        continue

            if valid_products:
                print(f"✅ Found {len(valid_products)} valid products.")
                return valid_products[:limit]
            else:
                print("⚠️ No valid products found in API response, using fallback.")
                return get_fallback_products(category)

        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:
                print(f"⚠️ Rate limited (429). Retrying in {wait_time}s...")
                time.sleep(wait_time)
                total_waited += wait_time
                wait_time = min(wait_time * 2, 10)
                retry += 1
            else:
                print(f"❌ HTTP error: {e}")
                break
        except requests.exceptions.RequestException as e:
            print(f"❌ Request exception: {e}")
            break

    print("❌ API fetch failed after retries. Using fallback products.")
    return get_fallback_products(category)

if __name__ == "__main__":
    print("🔍 Testing fetch for 'beauty' category...\n")
    products = fetch_best_sellers()

    if not products:
        print("❌ No products fetched.")
    else:
        for i, product in enumerate(products, 1):
            print(f"{i}. {product.get('title')}")
            print(f"   Link: {product.get('link')}")
            print(f"   Description: {product.get('description', 'No description available.')}\n")
