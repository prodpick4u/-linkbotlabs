from playwright.sync_api import sync_playwright

def get_top_3_products(url):
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
                print(f"Error: {e}")

        browser.close()

        if not products:
            raise Exception("No products found")

        return products
