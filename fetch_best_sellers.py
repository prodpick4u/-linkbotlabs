from dotenv import load_dotenv
load_dotenv()

import os
import requests
import time
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

AFFILIATE_TAG = os.getenv("AFFILIATE_TAG", "mychanneld-20")
ACTOR_ID = os.getenv("APIFY_ACTOR_ID", "epctex~google-search-scraper")
APIFY_TOKEN = os.getenv("APIFY_TOKEN")

print("🔍 fetch_best_sellers APIFY_TOKEN is set:", bool(APIFY_TOKEN))

def add_affiliate_tag(url):
    """Append or update the affiliate tag in the Amazon URL."""
    if "amazon." not in url:
        return url
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    query['tag'] = [AFFILIATE_TAG]
    new_query = urlencode(query, doseq=True)
    return urlunparse(parsed._replace(query=new_query))

def is_valid_amazon_product_url(url):
    """Check if URL is a valid Amazon product URL (contains /dp/)."""
    if not url or "amazon." not in url:
        return False
    return "/dp/" in url

def fetch_best_sellers(category="kitchen", limit=3, apify_token=None):
    token = apify_token or APIFY_TOKEN
    if not token:
        print("❌ Environment variable APIFY_TOKEN not set.")
        return []

    print(f"🔧 Starting Apify run for category '{category}' with token present: {bool(token)}")

    input_payload = {
        "csvFriendlyOutput": False,
        "customMapFunction": "(object) => { return {...object} }",
        "endPage": 1,
        "extendOutputFunction": """($) => {
            return {
                title: $("h3").first().text(),
                url: $("a").first().attr("href"),
                snippet: $("span").first().text()
            };
        }""",
        "includePeopleAlsoAsk": True,
        "includeUnfilteredResults": False,
        "locationUule": "w+CAIQICIIaXN0YW5idWw=",
        "maxItems": 20,
        "proxy": { "useApifyProxy": True },
        "queries": [category]
    }

    start_url = f"https://api.apify.com/v2/acts/{ACTOR_ID}/runs?token={token}"
    response = requests.post(start_url, json=input_payload)
    if not response.ok:
        print(f"❌ Failed to start Apify actor run: {response.text}")
        return []

    run_id = response.json()["data"]["id"]
    status_url = f"https://api.apify.com/v2/actor-runs/{run_id}?token={token}"

    while True:
        status_resp = requests.get(status_url)
        status = status_resp.json()["data"]["status"]
        if status in ["SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"]:
            break
        print(f"⌛ Apify run status: {status} (waiting 5s)")
        time.sleep(5)

    if status != "SUCCEEDED":
        print(f"❌ Apify run failed with status: {status}")
        return []

    dataset_id = status_resp.json()["data"]["defaultDatasetId"]
    dataset_url = f"https://api.apify.com/v2/datasets/{dataset_id}/items?token={token}&clean=true"
    dataset_resp = requests.get(dataset_url)
    if not dataset_resp.ok:
        print(f"❌ Failed to fetch Apify dataset: {dataset_resp.text}")
        return []

    items = dataset_resp.json()
    products = []

    for item in items:
        title = item.get("title")
        url = item.get("url", "")
        snippet = item.get("snippet", "")
        if title and is_valid_amazon_product_url(url):
            url_with_tag = add_affiliate_tag(url)
            products.append({
                "title": title.strip(),
                "link": url_with_tag,
                "price": "N/A",
                "image": "",
                "description": snippet
            })
        if len(products) >= limit:
            break

    # Fallback if fewer than limit products
    if len(products) < limit:
        print(f"⚠️ Only found {len(products)} valid products, adding fallback...")
        from fallback_products import get_fallback_products
        fallback = get_fallback_products(category)
        for fb_product in fallback:
            if len(products) >= limit:
                break
            products.append(fb_product)

    return products
