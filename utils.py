from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

def extract_image_urls(url, max_images=5):
    """
    Extract up to `max_images` images from a webpage.
    Converts relative URLs to absolute.
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        
        imgs = soup.find_all("img")
        urls = []
        for img in imgs:
            src = img.get("src")
            if src:
                img_url = urljoin(url, src)
                urls.append(img_url)
            if len(urls) >= max_images:
                break
        return urls
    except Exception as e:
        print(f"⚠️ Failed to extract images from {url}: {e}")
        return []
