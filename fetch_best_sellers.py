import os
import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

AFFILIATE_TAG = "mychanneld-20"
ACTOR_ID = os.getenv("APIFY_ACTOR_ID", "epctex~google-search-scraper")
APIFY_TOKEN = os.getenv("APIFY_TOKEN")

def add_affiliate_tag(url):
    """Append or update the affiliate tag in the Amazon URL."""
    if "amazon." not in url:
        return url  # Not an Amazon link

    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    query['tag'] = [AFFILIATE_TAG]
    new_query = urlencode(query, doseq=True)
    new_url = urlunparse(parsed._replace(query=new_query))
    return new_url

def fetch_best_sellers(category="kitchen", limit=3):
    if not APIFY_TOKEN:
        print("❌ APIFY_TOKEN not set in environment.")
        return []

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
        "proxy": {
            "useApifyProxy": True
        },
        "queries": [category]
    }

    # Start Apify actor run
    start_url = f"https://api.apify.com/v2/acts/{ACTOR_ID}/runs?token={APIFY_TOKEN}"
    response = requests.post(start_url, json=input_payload)
    if not response.ok:
        print(f"❌ Failed to start Apify actor run: {response.text}")
        return []
    run_id = response.json()["data"]["id"]

    # Poll until done
    status_url = f"https://api.apify.com/v2/actor-runs/{run_id}?token={APIFY_TOKEN}"
    while True:
        status_resp = requests.get(status_url)
        status = status_resp.json()["data"]["status"]
        if status in ["SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"]:
            break
        print(f"⌛ Apify run status: {status} (waiting 5s)")
        import time; time.sleep(5)

    if status != "SUCCEEDED":
        print(f"❌ Apify run failed with status: {status}")
        return []

    dataset_id = status_resp.json()["data"]["defaultDatasetId"]

    # Fetch dataset items
    dataset_url = f"https://api.apify.com/v2/datasets/{dataset_id}/items?token={APIFY_TOKEN}&clean=true"
    dataset_resp = requests.get(dataset_url)
    if not dataset_resp.ok:
        print(f"❌ Failed to fetch Apify dataset: {dataset_resp.text}")
        return []
    items = dataset_resp.json()

    # Filter & prepare products
    products = []
    for item in items[:limit]:
        title = item.get("title")
        url = add_affiliate_tag(item.get("url", ""))
        snippet = item.get("snippet", "")
        if title and url:
            products.append({
                "title": title.strip(),
                "link": url,
                "price": "N/A",           # Apify results may not include price — update if possible
                "image": "",              # Add if available
                "description": snippet
            })

    return products
