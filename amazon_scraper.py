import os
import requests
from playwright.sync_api import sync_playwright

def fetch_amazon_top3_with_fallback(search_url, category):
    try:
        print("🔍 Trying Playwright to scrape Amazon...")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(search_url, timeout=60000)

            page.wait_for_selector('div[data-component-type="s-search-result"]', timeout=15000)
            results = page.query_selector_all('div[data-component-type="s-search-result"]')

            top3 = []
            for result in results[:3]:
                title = result.query_selector('h2 span')?.inner_text() or "No Title"
                url = result.query_selector('h2 a')?.get_attribute("href")
                price_whole = result.query_selector('.a-price-whole')
                price_fraction = result.query_selector('.a-price-fraction')
                image = result.query_selector('img')?.get_attribute("src")

                price = "N/A"
                if price_whole and price_fraction:
                    price = f"${price_whole.inner_text()}.{price_fraction.inner_text()}"

                top3.append({
                    "title": title.strip(),
                    "price": price,
                    "image": image,
                    "url": f"https://www.amazon.com{url}" if url else None,
                })

            browser.close()

            if top3:
                return top3

        print("⚠️ No results from Playwright. Falling back to RapidAPI.")
    except Exception as e:
        print(f"⚠️ Playwright failed: {e}")

    # Fallback to RapidAPI
    return fetch_amazon_top3_from_rapidapi(category)


def fetch_amazon_top3_from_rapidapi(category="kitchen"):
    url = "https://amazon-online-data-api.p.rapidapi.com/product-search"
    querystring = {
        "country": "US",
        "keyword": category,
        "page": "1"
    }

    headers = {
        "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
        "X-RapidAPI-Host": "amazon-online-data-api.p.rapidapi.com"
    }

    try:
        print("🌐 Fetching from RapidAPI...")
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        data = response.json()

        if not data or "products" not in data or not data["products"]:
            print("❌ No products found in RapidAPI response.")
            return []

        top3 = data["products"][:3]
        return [{
            "title": item.get("title"),
            "image": item.get("main_image"),
            "price": item.get("price_str", "N/A"),
            "url": item.get("url"),
        } for item in top3]

    except Exception as e:
        print(f"❌ RapidAPI fetch failed: {e}")
        return []
