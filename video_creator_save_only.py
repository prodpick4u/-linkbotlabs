import os
from datetime import datetime
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip, TextClip
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = "static/output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_product_info(url):
    """
    Placeholder function: replace with real scraping or API later.
    Returns a dictionary with 'title' and 'description'.
    """
    # For now, extract a fake title from the URL
    title = f"Product: {url.split('/')[-1]}"
    description = "Amazing product! Check it out now!"
    return {"title": title, "description": description}

def create_text_image(text, width=1280, height=720, font_size=48):
    img = Image.new("RGB", (width, height), color=(30, 30, 30))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)
    except:
        font = ImageFont.load_default()

    lines = text.split('\n')
    y_text = (height - font_size * len(lines)) // 2
    for line in lines:
        text_width, text_height = draw.textsize(line, font=font)
        draw.text(((width - text_width) / 2, y_text), line, font=font, fill=(255, 255, 255))
        y_text += text_height + 10

    img_path = os.path.join(OUTPUT_DIR, f"frame_{datetime.now().strftime('%H%M%S%f')}.png")
    img.save(img_path)
    return img_path

def generate_audio(text):
    tts = gTTS(text=text)
    audio_path = os.path.join(OUTPUT_DIR, f"audio_{datetime.now().strftime('%H%M%S%f')}.mp3")
    tts.save(audio_path)
    return audio_path

def generate_video_from_urls(urls, duration_per_product=8):
    clips = []
    for url in urls:
        info = fetch_product_info(url)
        audio_text = f"{info['title']}. {info['description']}"
        audio_path = generate_audio(audio_text)
        img_path = create_text_image(f"{info['title']}\n\n{info['description']}")
        audio_clip = AudioFileClip(audio_path)
        img_clip = ImageClip(img_path).set_duration(duration_per_product).set_audio(audio_clip)
        clips.append(img_clip)

    final_clip = concatenate_videoclips(clips)
    
    # Optional watermark
    watermark = TextClip(
        "prodpick4u.com",
        fontsize=24,
        color="white",
        font="Arial-Bold",
        stroke_color="black",
        stroke_width=2,
        method="caption"
    ).set_duration(final_clip.duration).set_pos(("right","bottom")).margin(right=10, bottom=10)

    final_video = CompositeVideoClip([final_clip, watermark])

    output_path = os.path.join(OUTPUT_DIR, f"tiktok_video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4")
    final_video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")
    return output_path

# -------------------------
# Example usage
# -------------------------
if __name__ == "__main__":
    test_urls = [
        "https://www.amazon.com/dp/B09XYZ1234",
        "https://www.amazon.com/dp/B08ABC5678"
    ]
    video_file = generate_video_from_urls(test_urls)
    print(f"✅ Video generated: {video_file}")
