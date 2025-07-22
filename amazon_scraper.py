import os
import requests
from playwright.sync_api import sync_playwright

# Load RapidAPI key from env var
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = "amazon-product-search-api.p.rapidapi.com"

def get_products_by_asins(asins):
    """
    Fetch product info for a list of ASINs via RapidAPI Amazon API.
    """
    url = "https://amazon-product-search-api.p.rapidapi.com/products"
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }
    products = []
    for asin in asins:
        params = {"asin": asin}
        try:
            resp = requests.get(url, headers=headers, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            # Assuming response structure with product info in data['product'] or similar
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
            print(f"API fetch error for ASIN {asin}: {e}")
    return products

def get_top_3_products(url):
    """
    Scrape Amazon search page with Playwright, get top 3 products.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000)

        # Wait for product cards with new selector
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
                    "pros": "Popular choice",
                    "cons": "May be out of stock"
                })
            except Exception as e:
                print(f"Error scraping product: {e}")

        browser.close()

        if not products:
            raise Exception("No products found")

        return products

# Example usage:
if __name__ == "__main__":
    # Use Playwright scraper
    url = "https://www.amazon.com/s?k=outdoor+tents"
    try:
        products = get_top_3_products(url)
        print("Playwright scraped products:")
        for p in products:
            print(p)
    except Exception as e:
        print(f"Playwright scraping failed: {e}")
        # Fallback to API fetch with known ASINs if scraping fails
        example_asins = ["B08ZJTX8WZ", "B07YXL5GLM", "B07PZ4PK4R"]
        products = get_products_by_asins(example_asins)
        print("API fetched products:")
        for p in products:
            print(p)
