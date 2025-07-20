import os
import requests

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
YOUTUBE_CHANNEL_ID = 'UCy-zO_2DYOrWUlI0sYJR2ZQ'
AMAZON_ASSOCIATE_TAG = 'mychanneld-20'

def get_youtube_videos():
    url = f"https://www.googleapis.com/youtube/v3/search?key={YOUTUBE_API_KEY}&channelId={YOUTUBE_CHANNEL_ID}&part=snippet,id&order=date&maxResults=5"
    response = requests.get(url)
    data = response.json()
    videos = []
    for item in data.get('items', []):
        if item['id']['kind'] == 'youtube#video':
            video_id = item['id']['videoId']
            title = item['snippet']['title']
            videos.append({'id': video_id, 'title': title})
    return videos

products = [
    {'title': 'Samsung Galaxy Watch FE', 'asin': 'B0D13KX4D6'},
    {'title': 'Garmin Venu Sq 2', 'asin': 'B09N9Z4PY1'},
    {'title': 'Apple Watch SE (2nd Gen)', 'asin': 'B0BDJ6VQMW'}
]

def generate_blog_post(videos, products):
    html = "<html><head><title>Top Tech Products Reviewed</title></head><body>"
    html += "<h1>🔥 Best Tech Products with Reviews and Amazon Links</h1>"
    html += "<h2>🎥 Latest YouTube Reviews</h2>"
    for v in videos:
        html += f"<h3>{v['title']}</h3>"
        html += f'<iframe width="560" height="315" src="https://www.youtube.com/embed/{v["id"]}" frameborder="0" allowfullscreen></iframe>'
    html += "<h2>🛍️ Product Comparison</h2>"
    html += "<table border='1'><tr><th>Product</th><th>Buy on Amazon</th></tr>"
    for p in products:
        link = f"https://www.amazon.com/dp/{p['asin']}?tag={AMAZON_ASSOCIATE_TAG}"
        html += f"<tr><td>{p['title']}</td><td><a href='{link}' target='_blank'>Buy Now</a></td></tr>"
    html += "</table></body></html>"
    with open("top-products-review.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    videos = get_youtube_videos()
    generate_blog_post(videos, products)
