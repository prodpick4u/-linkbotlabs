import requests
import time
import json
import csv

# --- Configurable Variables ---
ACTOR_ID = "epctex~google-search-scraper"
TOKEN = "apify_api_86VfCoAQPrPyfZOrdqB5c2Ww6vYaQx0RqN8L"
OUTPUT_JSON = "results.json"
OUTPUT_CSV = "results.csv"

# --- Input Payload for Apify ---
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
    "queries": [
        "best sellers",
        "kitchen",
        "beauty",
        "outdoor",
        "tech",
        "household"
    ]
}

def start_apify_run():
    print("🔄 Starting Apify actor run...")
    start_url = f"https://api.apify.com/v2/acts/{ACTOR_ID}/runs?token={TOKEN}"
    response = requests.post(start_url, json=input_payload)
    data = response.json()
    if "data" not in data:
        raise Exception("Failed to start actor: " + str(data))
    return data["data"]["id"]

def wait_for_completion(run_id):
    status_url = f"https://api.apify.com/v2/actor-runs/{run_id}?token={TOKEN}"
    while True:
        resp = requests.get(status_url).json()
        status = resp["data"]["status"]
        print(f"⌛ Status: {status}")
        if status in ["SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"]:
            return resp
        time.sleep(5)

def fetch_dataset(dataset_id):
    print("📥 Fetching dataset results...")
    url = f"https://api.apify.com/v2/datasets/{dataset_id}/items?token={TOKEN}&clean=true"
    return requests.get(url).json()

def save_to_files(data):
    print(f"💾 Saving {len(data)} results to {OUTPUT_JSON} and {OUTPUT_CSV}")
    
    # Save to JSON
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Save to CSV
    if data:
        with open(OUTPUT_CSV, "w", newline='', encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

def main():
    try:
        run_id = start_apify_run()
        run_info = wait_for_completion(run_id)
        if run_info["data"]["status"] != "SUCCEEDED":
            print("❌ Run failed:", run_info["data"]["status"])
            return
        dataset_id = run_info["data"]["defaultDatasetId"]
        results = fetch_dataset(dataset_id)
        save_to_files(results)
        print("✅ Done.")
    except Exception as e:
        print("❗ Error:", str(e))

if __name__ == "__main__":
    main()
