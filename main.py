import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from blog_generator import generate_blog_post

if __name__ == "__main__":
    generate_blog_post()
    from utils.amazon_scraper import get_top_3_products
    category_url = "https://www.amazon.com/Best-Sellers-Kitchen/zgbs/kitchen"
top3 = get_top_3_products(category_url)

for product in top3:
    print(product["title"])
    print(product["link"])
    print(product["image"])
    print("-----")
