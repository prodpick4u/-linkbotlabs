import os
import requests
from bs4 import BeautifulSoup
from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip, TextClip
from gtts import gTTS
from io import BytesIO
from PIL import Image

# ----------------------------
# Download image from URL
# ----------------------------
def download_image(url, save_dir="static/output"):
    os.makedirs(save_dir, exist_ok=True)
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()
        ext = url.split(".")[-1].split("?")[0]
        filename = f"image_{os.urandom(4).hex()}.{ext}"
        path = os.path.join(save_dir, filename)
        with open(path, "wb") as f:
            f.write(response.content)
        return path
    except Exception as e:
        print(f"⚠️ Failed to download image: {e}")
        return None

# ----------------------------
# Extract title, description, main image from any URL
# ----------------------------
def fetch_page_info(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")
        title = soup.title.string.strip() if soup.title else "No Title"
        desc_tag = soup.find("meta", attrs={"name":"description"}) or soup.find("meta", attrs={"property":"og:description"})
        description = desc_tag["content"].strip() if desc_tag and "content" in desc_tag.attrs else ""
        img_tag = soup.find("meta", attrs={"property":"og:image"})
        image_url = img_tag["content"].strip() if img_tag and "content" in img_tag.attrs else None
        return {"title": title, "description": description, "image_url": image_url}
    except Exception as e:
        print(f"⚠️ Failed to fetch page info: {e}")
        return {"title": "No Title", "description": "", "image_url": None}

# ----------------------------
# Generate TTS audio
# ----------------------------
def generate_audio(script_text, save_dir="static/output"):
    os.makedirs(save_dir, exist_ok=True)
    audio_file = os.path.join(save_dir, f"audio_{os.urandom(4).hex()}.mp3")
    tts = gTTS(script_text)
    tts.save(audio_file)
    return audio_file

# ----------------------------
# Generate video from URLs
# ----------------------------
def generate_video_from_urls(urls, script_text="", output_path="static/output/video.mp4"):
    if not urls:
        raise ValueError("No URLs provided for video creation.")

    # Get page info from first URL
    page_info = fetch_page_info(urls[0])
    image_url = page_info.get("image_url")
    if not image_url:
        image_url = urls[0]  # fallback to URL itself if it is an image

    # Download image
    image_path = download_image(image_url)
    if not image_path:
        raise RuntimeError("Failed to download any image.")

    # Create audio from script or description
    if script_text:
        audio_path = generate_audio(script_text)
    else:
        combined_text = f"{page_info.get('title')} {page_info.get('description')}"
        audio_path = generate_audio(combined_text)

    audio_clip = AudioFileClip(audio_path)
    duration = audio_clip.duration

    # Create video
    resolution = (720, 1280)  # TikTok vertical
    image_clip = ImageClip(image_path).set_duration(duration).set_audio(audio_clip)
    image_clip = image_clip.resize(height=resolution[1])
    if image_clip.w > resolution[0]:
        image_clip = image_clip.resize(width=resolution[0])

    background = ImageClip(color=(0,0,0), size=resolution).set_duration(duration)
    video = CompositeVideoClip([background, image_clip.set_position("center")])

    # Overlay title text
    if page_info.get("title"):
        title_clip = TextClip(page_info["title"], fontsize=30, color="white", font="Arial-Bold", method="caption").set_duration(duration).set_position(("center","top"))
        video = CompositeVideoClip([video, title_clip])

    # Write final video
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    video.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=24, threads=4, verbose=True, logger=None)

    return output_path
