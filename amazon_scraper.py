import os
import requests
from playwright.sync_api import sync_playwright

# RapidAPI details from environment
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST", "real-time-amazon-data.p.rapidapi.com")

def fetch_products_from_rapidapi(category="kitchen"):
    url = "https://real-time-amazon-data.p.rapidapi.com/bestsellers"
    querystring = {"category": category, "country": "US"}
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }
    try:
        resp = requests.get(url, headers=headers, params=querystring, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        products = []
        for item in data.get("body", [])[:3]:
            products.append({
                "title": item.get("product_title", "No title"),
                "link": item.get("product_url", ""),
                "image": item.get("product_photo", ""),
                "price": item.get("product_price", "Price not available"),
                "rating": item.get("product_star_rating", "No rating"),
                "pros": "API fetched product",
                "cons": None
            })
        return products
    except Exception as e:
        print(f"❌ RapidAPI fetch failed: {e}")
        return []

def fetch_products_from_playwright(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000)
        page.wait_for_selector('div[data-component-type="s-search-result"]', timeout=30000)

        items = page.query_selector_all('div[data-component-type="s-search-result"]')[:3]

        products = []
        for item in items:
            try:
                title = item.query_selector("h2 a span")
                link = item.query_selector("h2 a")
                img = item.query_selector("img.s-image")
                price = item.query_selector("span.a-price > span.a-offscreen")

                products.append({
                    "title": title.inner_text().strip() if title else "No title",
                    "link": "https://www.amazon.com" + link.get_attribute("href") if link else "",
                    "image": img.get_attribute("src") if img else "",
                    "price": price.inner_text().strip() if price else "Price not available",
                    "rating": "N/A",
                    "pros": "Popular choice",
                    "cons": "May be out of stock"
                })
            except Exception as e:
                print(f"⚠️ Playwright parse error: {e}")

        browser.close()

        if not products:
            raise Exception("No products found with Playwright")

        return products

def fetch_amazon_top3_with_fallback(url, category="kitchen"):
    """
    Try Playwright scraping first. If it fails, fallback to RapidAPI.
    """
    try:
        print("🔍 Trying Playwright scraping...")
        products = fetch_products_from_playwright(url)
        print("✅ Playwright succeeded.")
        return products
    except Exception as e:
        print(f"⚠️ Playwright failed: {e}")
        print("📦 Falling back to RapidAPI...")
        products = fetch_products_from_rapidapi(category)
        if not products:
            print("❌ RapidAPI also failed.")
        else:
            print("✅ RapidAPI succeeded.")
        return products

# For quick testing
if __name__ == "__main__":
    amazon_search_url = "https://www.amazon.com/s?k=kitchen"
    products = fetch_amazon_top3_with_fallback(amazon_search_url, category="kitchen")

    print("\n🛒 Top 3 Products:")
    for i, p in enumerate(products, 1):
        print(f"{i}. {p['title']}")
        print(f"   Price: {p['price']}")
        print(f"   Link: {p['link']}")
        print(f"   Pros: {p.get('pros')}")
        print(f"   Cons: {p.get('cons')}\n")
