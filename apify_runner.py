import os
import time
import requests
import json

# Load API credentials from environment
APIFY_TOKEN = os.getenv("APIFY_TOKEN")
ACTOR_ID = os.getenv("APIFY_ACTOR_ID", "jm4192gDoX7CHY7IB")  # Replace with your actor ID or keep as default

# Define your input for the actor
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

def run_apify_actor(input_payload):
    start_url = f"https://api.apify.com/v2/acts/{ACTOR_ID}/runs"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {APIFY_TOKEN}"
    }

    print("🚀 Triggering Apify actor...")
    response = requests.post(start_url, headers=headers, json=input_payload)  # ✅ Fixed line
    response.raise_for_status()
    run_id = response.json()["data"]["id"]

    # Poll until actor run is finished
    status_url = f"https://api.apify.com/v2/actor-runs/{run_id}"
    while True:
        status_response = requests.get(status_url, headers=headers)
        status_response.raise_for_status()
        status = status_response.json()["data"]["status"]
        if status in ["SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"]:
            break
        print(f"⏳ Waiting for Apify run {run_id}... status: {status}")
        time.sleep(5)

    if status != "SUCCEEDED":
        raise Exception(f"Apify run failed with status: {status}")

    # Fetch output dataset
    dataset_id = status_response.json()["data"]["defaultDatasetId"]
    dataset_url = f"https://api.apify.com/v2/datasets/{dataset_id}/items?format=json"
    print(f"📦 Fetching results from dataset {dataset_id}...")
    dataset_response = requests.get(dataset_url)
    dataset_response.raise_for_status()

    return dataset_response.json()

def main():
    try:
        results = run_apify_actor(input_payload)
        with open("apify_results.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print("✅ Apify results saved to apify_results.json")
    except Exception as e:
        print("❌ Error running Apify actor:", e)

if __name__ == "__main__":
    main()
