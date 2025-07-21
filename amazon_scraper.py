from playwright.sync_api import sync_playwright

def get_top_3_products(category_url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(category_url, timeout=60000)

        # Wait for product containers
        page.wait_for_selector('div.p13n-sc-uncoverable-faceout')

        product_elements = page.query_selector_all('div.p13n-sc-uncoverable-faceout')[:3]

        top_products = []
        for element in product_elements:
            try:
                title = element.query_selector('._cDEzb_p13n-sc-css-line-clamp-3_g3dy1')
                title_text = title.inner_text().strip() if title else "No title"

                link_elem = element.query_selector('a.a-link-normal')
                link_href = "https://www.amazon.com" + link_elem.get_attribute('href') if link_elem else ""

                img_elem = element.query_selector('img')
                img_src = img_elem.get_attribute('src') if img_elem else ""

                price_elem = element.query_selector('span.a-price span.a-offscreen')
                price = price_elem.inner_text().strip() if price_elem else "Price not available"

                top_products.append({
                    "title": title_text,
                    "link": link_href,
                    "image": img_src,
                    "price": price,
                    "pros": "Popular and high-quality.",
                    "cons": "Might sell out quickly."
                })
            except Exception as e:
                print(f"Error parsing product: {e}")

        browser.close()

        if not top_products:
            raise Exception("No products found.")

        return top_products
