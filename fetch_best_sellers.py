import requests
import os
import time
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode

from fallback_products import get_fallback_products  # Import fallback

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "your_default_key")
AMAZON_TAG = os.getenv("AMAZON_TAG", "mychanneld-20")

def add_affiliate_tag(url, tag):
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    query['tag'] = tag
    new_query = urlencode(query, doseq=True)
    return urlunparse(parsed._replace(query=new_query))

def fetch_best_sellers(category="beauty", country="us", page=1, limit=3, max_retries=5):
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

    retry = 0
    wait_time = 2  # seconds before first retry

    while retry < max_retries:
        try:
            response = requests.get(url, headers=headers, params=params)
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
                else:
                    continue

            if valid_products:
                return valid_products[:limit]
            else:
                print("⚠️ No valid products found from API, using fallback products.")
                return get_fallback_products(category)

        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:
                print(f"⚠️ Rate limited by API. Retry {retry + 1}/{max_retries} after {wait_time} seconds...")
                time.sleep(wait_time)
                wait_time *= 2  # exponential backoff
                retry += 1
            else:
                print(f"❌ HTTP error: {e}")
                break
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
            break

    print(f"❌ Failed to fetch products after {max_retries} retries. Using fallback products.")
    return get_fallback_products(category)

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
