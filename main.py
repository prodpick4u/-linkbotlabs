from amazon_scraper import get_top_3_products

def main():
    url = "https://www.amazon.com/Best-Sellers-Kitchen/zgbs/kitchen"
    print("🔍 Fetching top 3 products...\n")
    try:
        products = get_top_3_products(url)
        for i, product in enumerate(products, start=1):
            print(f"{i}. {product['title']}")
            print(f"   Price: {product['price']}")
            print(f"   Link: {product['link']}")
            print()
    except Exception as e:
        print(f"❌ Failed to fetch products: {e}")

if __name__ == "__main__":
    main()
