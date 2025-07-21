import requests
from bs4 import BeautifulSoup

def get_top_3_products(category_keyword):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        )
    }

    search_url = f"https://www.amazon.com/s?k={category_keyword}"
    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch page: {response.status_code}")

    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.select('div.p13n-sc-uncoverable-faceout')[:3]

    top_products = []
    for item in items:
        try:
            title = item.select_one('._cDEzb_p13n-sc-css-line-clamp-3_g3dy1').text.strip()
            link = "https://www.amazon.com" + item.select_one('a.a-link-normal')['href']
            image = item.select_one('img')['src']
            top_products.append({
                "title": title,
                "link": link,
                "image": image
            })
        except Exception as e:
            print(f"Skipping item due to parsing error: {e}")

    return top_products
