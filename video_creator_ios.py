import os
from moviepy.editor import *
from datetime import datetime

# ========== CONFIG ==========
OS_TYPE = 'mac'  # or 'windows'
UPLOAD_AUTOMATICALLY = False  # Leave off for now

VIDEO_TITLE = "Top 3 Tents of 2025"
FILENAME = f"camping_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"

# Save to iCloud Drive (so you can see it in Files app on iPhone)
SAVE_TO_ICLOUD = True

if OS_TYPE == 'mac':
    if SAVE_TO_ICLOUD:
        OUTPUT_PATH = os.path.expanduser(f"~/Library/Mobile Documents/com~apple~CloudDocs/{FILENAME}")
    else:
        OUTPUT_PATH = os.path.expanduser(f"~/Desktop/{FILENAME}")
else:
    OUTPUT_PATH = os.path.join(os.environ["USERPROFILE"], "Desktop", FILENAME)

# ========== STEP 1: GENERATE VIDEO ==========
clip = TextClip(VIDEO_TITLE, fontsize=60, color='white', size=(1280, 720)).set_duration(5)

clip.write_videofile(OUTPUT_PATH, fps=24)
print(f"✅ Video saved to: {OUTPUT_PATH}")

# ========== STEP 2: Manual upload ==========
print("📱 You can now open the Files app on your iPhone and upload from iCloud or AirDrop the file from Desktop.")
