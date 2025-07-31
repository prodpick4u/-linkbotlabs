import os
import time
import requests
import json
from dotenv import load_dotenv

# === LOAD ENVIRONMENT ===
load_dotenv()
APIFY_TOKEN = os.getenv("APIFY_TOKEN")
ACTOR_ID = "V8SFJw3gKgULelpok"  # ✅ Your Apify Actor ID

# === INPUT PAYLOAD FOR ACTOR ===
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
    "locationUule": "w+CAIQICIIaXN0YW5idWw=",  # Thailand region
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

# === RUN APIFY ACTOR ===
def run_apify_actor(payload):
    if not APIFY_TOKEN:
        raise EnvironmentError("❌ APIFY_TOKEN is missing in environment variables.")

    start_url = f"https://api.apify.com/v2/acts/{ACTOR_ID}/runs"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {APIFY_TOKEN}"
    }

    print("🚀 Triggering Apify actor...")
    response = requests.post(start_url, headers=headers, json=payload)
    response.raise_for_status()

    run_data = response.json().get("data", {})
    run_id = run_data.get("id")
    if not run_id:
        raise ValueError("❌ No run ID returned from Apify.")

    # === POLL FOR COMPLETION ===
    status_url = f"https://api.apify.com/v2/actor-runs/{run_id}"
    while True:
        time.sleep(5)
        status_response = requests.get(status_url, headers=headers)
        status_response.raise_for_status()
        status_data = status_response.json().get("data", {})
        status = status_data.get("status")
        print(f"⏳ Actor status: {status}")
        if status in ["SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"]:
            break

    if status != "SUCCEEDED":
        raise RuntimeError(f"❌ Actor run failed with status: {status}")

    # === GET RESULTS FROM DATASET ===
    dataset_id = status_data.get("defaultDatasetId")
    if not dataset_id:
        raise ValueError("❌ Dataset ID not found in actor run response.")

    dataset_url = f"https://api.apify.com/v2/datasets/{dataset_id}/items?format=json"
    print(f"📦 Fetching dataset results from: {dataset_url}")
    dataset_response = requests.get(dataset_url)
    dataset_response.raise_for_status()
    return dataset_response.json()

# === MAIN ENTRY POINT ===
def main():
    try:
        results = run_apify_actor(input_payload)

        with open("apify_results.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        print("✅ Results saved to apify_results.json")

        print("🔍 Sample results:")
        for item in results[:3]:
            title = item.get("title", "No title")
            url = item.get("url", "No URL")
            print(f"• {title} → {url}")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
