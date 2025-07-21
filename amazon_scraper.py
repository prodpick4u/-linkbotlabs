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
                
                # Updated selector for best seller items
                items = soup.select('div.zg-item-immersion')[:3]

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
