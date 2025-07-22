import os
from moviepy.editor import *
from datetime import datetime

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

FILENAME = f"camping_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, FILENAME)

clip = TextClip("Top 3 Tents of 2025", fontsize=60, color='white', size=(1280, 720)).set_duration(5)
clip.write_videofile(OUTPUT_PATH, fps=24)

print(f"✅ Video saved at {OUTPUT_PATH}")
