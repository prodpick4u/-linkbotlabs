import os
import requests
from playwright.sync_api import sync_playwright

# Load RapidAPI credentials
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = "amazon-product-search-api.p.rapidapi.com"

def get_products_by_asins(asins):
    """
    Fetch product info for a list of ASINs via RapidAPI Amazon API.
    """
    url = "https://amazon-product-search-api.p.rapidapi.com/product-details"
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }

    products = []
    for asin in asins:
        params = {"asin": asin}
        try:
            print(f"🔗 Fetching ASIN {asin} using: {url}")
            resp = requests.get(url, headers=headers, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            product = data.get('product', {})
            products.append({
                "title": product.get("title", "No title"),
                "link": f"https://www.amazon.com/dp/{asin}",
                "image": product.get("image", ""),
                "price": product.get("price", "Price not available"),
                "rating": product.get("rating", "No rating"),
                "pros": "API fetched product",
                "cons": "Limited info"
            })
        except Exception as e:
            print(f"❌ API fetch error for ASIN {asin}: {e}")
    return products

def get_top_3_products(url):
    """
    Scrape Amazon search page using Playwright, return top 3 products.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000)
        page.wait_for_selector('div[data-component-type="s-search-result"]')

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
                print(f"⚠️ Error parsing product block: {e}")

        browser.close()

        if not products:
            raise Exception("No products found with Playwright")

        return products

def fetch_amazon_top3_with_fallback(url, fallback_asins):
    """
    Try Playwright scraping first. If it fails, use RapidAPI with known ASINs.
    """
    try:
        print("🔍 Trying Playwright scraping...")
        products = get_top_3_products(url)
        print("✅ Playwright succeeded.")
        return products
    except Exception as e:
        print(f"⚠️ Playwright failed: {e}")
        print("📦 Falling back to RapidAPI...")
        products = get_products_by_asins(fallback_asins)
        if not products:
            print("❌ RapidAPI also failed.")
        else:
            print("✅ RapidAPI succeeded.")
        return products

# For testing or running as a script
if __name__ == "__main__":
    search_url = "https://www.amazon.com/s?k=outdoor+tents"
    known_asins = ["B08ZJTX8WZ", "B07YXL5GLM", "B07PZ4PK4R"]

    final_products = fetch_amazon_top3_with_fallback(search_url, known_asins)

    print("\n🛒 Final Product List:")
    for idx, product in enumerate(final_products, 1):
        print(f"{idx}. {product['title']}")
        print(f"   Price: {product['price']}")
        print(f"   Link: {product['link']}\n")
