import os
import requests

def fetch_best_sellers(category="mobile-apps", country="us", page=1):
    url = "https://realtime-amazon-data.p.rapidapi.com/best-sellers"
    headers = {
        "x-rapidapi-host": "realtime-amazon-data.p.rapidapi.com",
        "x-rapidapi-key": "1cd005eae7msh84dc8a952496e8ap11a8c8jsn1d76048c3e91"
    }
    params = {
        "category": category,
        "country": country,
        "page": page
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print(f"API error {response.status_code}: {response.text}")
        return []

    data = response.json()
    return data  # or parse it however you need

if __name__ == "__main__":
    products = fetch_best_sellers()
    print(products)
