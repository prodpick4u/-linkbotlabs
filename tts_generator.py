from gtts import gTTS

def generate_voiceover(text, lang='en'):
    tts = gTTS(text, lang=lang)
    path = "output.mp3"
    tts.save(path)
    return path