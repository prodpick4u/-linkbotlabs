import os
import time
import requests

APIFY_TOKEN = os.getenv("APIFY_TOKEN")
ACTOR_ID = os.getenv("APIFY_ACTOR_ID", "jm4192gDoX7CHY7IB")

def run_apify_actor(input_payload):
    # Start actor
    start_url = f"https://api.apify.com/v2/acts/{ACTOR_ID}/runs"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {APIFY_TOKEN}"
    }

    print("🚀 Triggering Apify actor...")
    response = requests.post(start_url, headers=headers, json={"input": input_payload})
    response.raise_for_status()
    run_id = response.json()["data"]["id"]

    # Poll for finish
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

    # Fetch dataset items
    dataset_id = status_response.json()["data"]["defaultDatasetId"]
    dataset_url = f"https://api.apify.com/v2/datasets/{dataset_id}/items?format=json"
    print(f"📦 Fetching results from dataset {dataset_id}...")
    dataset_response = requests.get(dataset_url)
    dataset_response.raise_for_status()

    return dataset_response.json()
