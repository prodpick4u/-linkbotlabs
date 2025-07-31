import os
import time
import requests
import json

# === CONFIGURATION ===
APIFY_TOKEN = os.getenv("APIFY_TOKEN")
ACTOR_ID = "V8SFJw3gKgULelpok"  # ✅ Your specific Apify Actor ID

# === INPUT PAYLOAD FOR ACTOR ===
input_payload = {
    "csvFriendlyOutput": False,
    "customMapFunction": "(object) => { return {...object} }",
    "endPage": 1,
    "extendOutputFunction": """($) => {
        return {
            title: $('h3').first().text(),
            url: $('a').first().attr('href'),
            snippet: $('div span').first().text()
        };
    }""",
    "includePeopleAlsoAsk": True,
    "includeUnfilteredResults": False,
    "locationUule": "w+CAIQICIIaXN0YW5idWw=",  # Bangkok
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

# === RUNNER FUNCTION ===
def run_apify_actor(input_payload):
    if not APIFY_TOKEN:
        raise EnvironmentError("❌ APIFY_TOKEN is not set in environment variables.")

    start_url = f"https://api.apify.com/v2/acts/{ACTOR_ID}/runs"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {APIFY_TOKEN}"
    }

    print("🚀 Triggering Apify actor...")
    try:
        response = requests.post(start_url, headers=headers, json=input_payload)
        response.raise_for_status()
        run_id = response.json()["data"]["id"]
    except Exception as e:
        raise RuntimeError(f"❌ Failed to trigger Apify actor: {e}")

    # === POLL FOR STATUS ===
    status_url = f"https://api.apify.com/v2/actor-runs/{run_id}"
    while True:
        try:
            status_response = requests.get(status_url, headers=headers)
            status_response.raise_for_status()
            status = status_response.json()["data"]["status"]
            if status in ["SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"]:
                break
            print(f"⏳ Waiting... Actor status: {status}")
            time.sleep(5)
        except Exception as e:
            raise RuntimeError(f"❌ Error checking actor status: {e}")

    if status != "SUCCEEDED":
        raise RuntimeError(f"❌ Apify run failed with status: {status}")

    # === FETCH RESULTS ===
    try:
        dataset_id = status_response.json()["data"]["defaultDatasetId"]
        dataset_url = f"https://api.apify.com/v2/datasets/{dataset_id}/items?format=json"
        print(f"📦 Fetching results from dataset {dataset_id}...")
        dataset_response = requests.get(dataset_url)
        dataset_response.raise_for_status()
        return dataset_response.json()
    except Exception as e:
        raise RuntimeError(f"❌ Failed to fetch Apify dataset: {e}")

# === MAIN EXECUTION ===
def main():
    try:
        results = run_apify_actor(input_payload)
        with open("apify_results.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print("✅ Apify results saved to apify_results.json")

        # Optional preview of first 3 items
        print("🔍 Sample results:")
        for item in results[:3]:
            print(f"• {item.get('title')} → {item.get('url')}")
    except Exception as e:
        print("❌ Error:", e)

if __name__ == "__main__":
    main()
