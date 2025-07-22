import os
from datetime import datetime
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont

# Create output folder
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Create image with text
img = Image.new("RGB", (1280, 720), color=(0, 0, 0))
draw = ImageDraw.Draw(img)

# Use a built-in font or fallback
try:
    font = ImageFont.truetype("DejaVuSans-Bold.ttf", 60)
except:
    font = ImageFont.load_default()

text = "Top 3 Tents of 2025"
text_width, text_height = draw.textsize(text, font=font)
draw.text(
    ((1280 - text_width) / 2, (720 - text_height) / 2),
    text,
    font=font,
    fill=(255, 255, 255)
)

image_path = os.path.join(OUTPUT_DIR, "frame.png")
img.save(image_path)

# Create video from image
clip = ImageClip(image_path).set_duration(5)
filename = f"camping_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
output_path = os.path.join(OUTPUT_DIR, filename)
clip.write_videofile(output_path, fps=24)

print(f"✅ Video saved at {output_path}")
