import os
import re
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

# ✅ Your Amazon Affiliate Tag
AFFILIATE_TAG = "mychanneld-20"

def extract_asin(url):
    if not url:
        return None
    match = re.search(r"/dp/([A-Z0-9]{10})|/gp/product/([A-Z0-9]{10})", url)
    if match:
        return match.group(1) or match.group(2)
    return None

def make_affiliate_link(url):
    asin = extract_asin(url)
    if asin:
        return f"https://www.amazon.com/dp/{asin}?tag={AFFILIATE_TAG}"
    return url or "#"

def prepare_products(products):
    for product in products:
        product['affiliate_link'] = make_affiliate_link(product.get('link') or product.get('url'))
    return products

def generate_markdown(products, category_title):
    products = prepare_products(products)
    markdown = f"# {category_title}\n\n"
    for product in products:
        markdown += f"## [{product['title']}]({product['affiliate_link']})\n"
        markdown += f"- **Price:** {product['price']}\n"
        markdown += f"- **Description:** {product.get('description', 'No description')}\n\n"
    return markdown

def generate_html(products, category_title, template_path, category_description=""):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(base_dir, "templates")
    env = Environment(loader=FileSystemLoader(templates_dir))

    template_name = os.path.basename(template_path)

    try:
        template = env.get_template(template_name)
    except TemplateNotFound:
        print(f"❌ Template '{template_name}' not found in '{templates_dir}'.")
        raise

    products = prepare_products(products)

    return template.render(
        category_title=category_title,
        products=products,
        category_description=category_description
    )

def save_blog_files(category_title, markdown, html, html_filename):
    if isinstance(html_filename, list):
        html_filename = html_filename[0]  # Just in case it’s accidentally passed as a list

    slug = html_filename.replace(".html", "")
    md_filename = f"docs/blog_{slug}.md"          # Save markdown inside docs/
    html_output_path = f"docs/{html_filename}"    # Save HTML inside docs/

    os.makedirs(os.path.dirname(md_filename), exist_ok=True)
    os.makedirs(os.path.dirname(html_output_path), exist_ok=True)

    with open(md_filename, "w", encoding="utf-8") as f:
        f.write(markdown)

    with open(html_output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"📝 Saved Markdown: {md_filename}")
    print(f"🌐 Saved HTML: {html_output_path}")
