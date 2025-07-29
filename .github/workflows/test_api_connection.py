import requests
import os

url = "https://real-time-amazon-data5.p.rapidapi.com/search"
querystring = {
    "query": "laptop",
    "page": "1",
    "country": "US"
}

headers = {
    "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),  # Or paste your key directly for testing
    "X-RapidAPI-Host": "real-time-amazon-data5.p.rapidapi.com"
}

try:
    response = requests.get(url, headers=headers, params=querystring)
    response.raise_for_status()
    data = response.json()
    print("✅ API call successful. Found products:")
    for item in data.get("data", {}).get("products", [])[:3]:
        print(f"- {item.get('title')}")
except requests.exceptions.HTTPError as err:
    print("❌ HTTP Error:", err)
    print("Response content:", response.text)
except Exception as e:
    print("❌ Error:", e)
