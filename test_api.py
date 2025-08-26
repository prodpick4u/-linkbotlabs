import requests

RAPIDAPI_KEY = "1cd005eae7msh84dc8a952496e8ap11a8c8jsn1d76048c3e91"

def test_fetch():
    url = "https://realtime-amazon-data.p.rapidapi.com/best-sellers"
    headers = {
        "x-rapidapi-host": "realtime-amazon-data.p.rapidapi.com",
        "x-rapidapi-key": RAPIDAPI_KEY
    }
    params = {
        "category": "beauty",
        "country": "us",
        "page": 1
    }
    response = requests.get(url, headers=headers, params=params)
    print("Status code:", response.status_code)
    print("Response body:", response.text)

if __name__ == "__main__":
    test_fetch()
