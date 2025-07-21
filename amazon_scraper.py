from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def fetch_page_html(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # headless=True means no GUI
        page = browser.new_page()
        page.goto(url, timeout=60000)  # 60 seconds timeout
        page.wait_for_timeout(5000)  # wait 5 seconds to allow JS to load
        content = page.content()
        browser.close()
        return content

def get_top_3_products_amazon(url):
    html = fetch_page_html(url)
    soup = BeautifulSoup(html, 'html.parser')

    # Try selectors for best seller items
    items = soup.select('li.zg-item-immersion')[:3]
    if not items:
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

    return top_products

if __name__ == "__main__":
    url = "https://www.amazon.com/Best-Sellers-Kitchen/zgbs/kitchen"
    products = get_top_3_products_amazon(url)
    for i, p in enumerate(products, 1):
        print(f"{i}. {p['title']}")
        print(f"   Price: {p['price']}")
        print(f"   Link: {p['link']}")
        print(f"   Image: {p['image']}")
        print()
