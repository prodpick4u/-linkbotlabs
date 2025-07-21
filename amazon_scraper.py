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

    for attempt in range(3):
        try:
            print(f"Attempt {attempt + 1}: Fetching {category_url}")
            response = requests.get(category_url, headers=headers)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                items = soup.select('div.p13n-sc-uncoverable-faceout')[:3]

                top_products = []
                for item in items:
                    try:
                        title = item.select_one('._cDEzb_p13n-sc-css-line-clamp-3_g3dy1').text.strip()
                        link = "https://www.amazon.com" + item.select_one('a.a-link-normal')['href']
                        image = item.select_one('img')['src']
                        price_tag = item.select_one('span.a-price > span.a-offscreen')
                        price = price_tag.text.strip() if price_tag else "Price not available"

                        top_products.append({
                            "title": title,
                            "link": link,
                            "image": image,
                            "price": price,
                            "pros": "Great performance and value.",
                            "cons": "May not suit all needs."
                        })
                    except Exception as e:
                        print(f"Skipping item due to parsing error: {e}")

                return top_products

            else:
                print(f"Attempt {attempt + 1}: Status {response.status_code}")
                time.sleep(random.uniform(2, 4))  # Wait and retry
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(random.uniform(2, 4))

    raise Exception("Failed to fetch page after 3 attempts")
