from gtts import gTTS
import os
import time
import platform

def generate_tts(text, lang='en', filename='output.mp3'):
    try:
        tts = gTTS(text, lang=lang)
        tts.save(filename)
        print(f"✅ Saved TTS to: {filename}")
        return filename
    except Exception as e:
        print(f"❌ Error generating TTS: {e}")
        return None

def play_audio(file_path):
    system = platform.system()
    try:
        if system == "Darwin":  # macOS
            os.system(f"afplay '{file_path}'")
        elif system == "Windows":
            os.system(f'start /min wmplayer "{file_path}"')
        elif system == "Linux":
            os.system(f"mpg123 '{file_path}'")
        else:
            print("🚫 Audio playback not supported on this OS.")
    except Exception as e:
        print(f"❌ Error playing audio: {e}")

def batch_generate(text_list):
    paths = []
    for i, text in enumerate(text_list, 1):
        filename = f"tts_output_{i}.mp3"
        path = generate_tts(text, filename=filename)
        if path:
            paths.append(path)
    return paths

def play_all_audio(files):
    print("▶️ Playing all TTS files once...")
    for file_path in files:
        play_audio(file_path)
        time.sleep(1.5)  # Optional pause between clips

# 📝 Example usage
product_scripts = [
    "Discover the best kitchen gadgets for 2025, handpicked daily to boost your cooking game.",
    "Explore trending outdoor gear to make your next adventure more fun and safe.",
    "Get the top beauty products of 2025, reviewed and recommended just for you!"
]

tts_files = batch_generate(product_scripts)
play_all_audio(tts_files)
