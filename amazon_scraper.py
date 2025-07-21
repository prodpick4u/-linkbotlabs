import requests
from bs4 import BeautifulSoup
import time
import random

def get_top_3_products(category_url):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        )
    }

    # Retry up to 3 times if 503 or other issues
    for attempt in range(3):
        try:
            response = requests.get(category_url, headers=headers, timeout=10)
            if response.status_code == 200:
                break
            else:
                print(f"Attempt {attempt+1}: Status {response.status_code}")
                time.sleep(2 + random.random() * 2)
        except Exception as e:
            print(f"Attempt {attempt+1} failed: {e}")
            time.sleep(2 + random.random() * 2)
    else:
        raise Exception(f"Failed to fetch page after 3 attempts")

    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.select('div.p13n-sc-uncoverable-faceout')[:3]

    top_products = []
    for item in items:
        try:
            title = item.select_one('._cDEzb_p13n-sc-css-line-clamp-3_g3dy1').text.strip()
            link = "https://www.amazon.com" + item.select_one('a.a-link-normal')['href']
            if "?tag=" not in link:
                link += "?tag=mychanneld-20"  # <-- Add your affiliate tag here
            image = item.select_one('img')['src']
            top_products.append({
                "title": title,
                "link": link,
                "image": image
            })
        except Exception as e:
            print(f"Skipping item due to parsing error: {e}")

    return top_products
