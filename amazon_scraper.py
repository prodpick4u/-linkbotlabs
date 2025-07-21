import requests
from bs4 import BeautifulSoup
import time
import random

def get_top_3_products(category_url):
    session = requests.Session()

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "DNT": "1",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    }

    for attempt in range(3):
        try:
            print(f"Attempt {attempt + 1}: Fetching {category_url}")
            response = session.get(category_url, headers=headers, timeout=10)

            if response.status_code == 200:
                html = response.text
                print("Response HTML preview:")
                print(html[:2000])  # debug print

                soup = BeautifulSoup(html, 'html.parser')

                items = soup.select('li.zg-item-immersion')[:3]
                if not items:
                    print("No 'li.zg-item-immersion' found, trying div.zg-item-immersion")
                    items = soup.select('div.zg-item-immersion')[:3]
                if not items:
                    print("No product items found with current selectors.")
                    return []

                top_products = []
                for item in items:
                    try:
                        title_tag = item.select_one('div.p13n-sc-truncate-desktop-type2, div.p13n-sc-truncated')
                        title = title_tag.text.strip() if title_tag else "No title"

                        link_tag = item.select_one('a.a-link-normal')
                        link = "https://www.amazon.com" + link_tag['href'] if link_tag else "#"

                        img_tag = item.select_one('img')
                        image = img_tag['src'] if img_tag else ""

                        price_tag = item.select_one('span.p13n-sc-price')
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

                if len(top_products) == 0:
                    print("No products found with updated selectors.")
                    return []

                return top_products

            else:
                print(f"Attempt {attempt + 1}: Status {response.status_code}")
                time.sleep(random.uniform(2, 4))  # Wait and retry

        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(random.uniform(2, 4))

    raise Exception("Failed to fetch page after 3 attempts")
