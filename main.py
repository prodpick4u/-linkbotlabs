import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from blog_generator import generate_blog_post

if __name__ == "__main__":
    generate_blog_post()
    from utils.amazon_scraper import get_top_3_products
    category_url = "https://www.amazon.com/Best-Sellers-Kitchen/zgbs/kitchen"
top3 = get_top_3_products(category_url)
# 1. Choose a category URL
category_url = "https://www.amazon.com/Best-Sellers-Kitchen/zgbs/kitchen"

# 2. Get top 3 products
top_products = get_top_3_products(category_url)

# 3. Format blog content
blog_content = "\n\n".join([
    f"### {i+1}. {p['title']}\n[Buy Here]({p['link']})\n![Image]({p['image']})"
    for i, p in enumerate(top_products)
])

# 4. Save blog to markdown
with open("top3_blog.md", "w", encoding="utf-8") as f:
    f.write("# Today's Top 3 Amazon Products\n\n" + blog_content)

for product in top3:
    print(product["title"])
    print(product["link"])
    print(product["image"])
    print("-----")
