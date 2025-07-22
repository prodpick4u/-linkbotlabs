import os
from datetime import datetime
from moviepy.editor import ImageClip
from PIL import Image, ImageDraw, ImageFont

# Create output directory
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Create image with Pillow
img = Image.new("RGB", (1280, 720), color=(30, 30, 30))
draw = ImageDraw.Draw(img)

text = "Top 3 Tents of 2025"
font = ImageFont.truetype("DejaVuSans-Bold.ttf", 60)
text_width, text_height = draw.textsize(text, font=font)
draw.text(((1280 - text_width)/2, (720 - text_height)/2), text, font=font, fill=(255, 255, 255))

img_path = os.path.join(OUTPUT_DIR, "frame.png")
img.save(img_path)

# Convert image to video
clip = ImageClip(img_path).set_duration(5)
video_path = os.path.join(OUTPUT_DIR, f"camping_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4")
clip.write_videofile(video_path, fps=24)
