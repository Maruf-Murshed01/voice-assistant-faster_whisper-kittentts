from faster_whisper import WhisperModel
from kittentts import KittenTTS
import soundfile as sf
import os

model_stt = WhisperModel("base")
model_tts = KittenTTS("KittenML/kitten-tts-mini-0.8")

def listen():
    """Record audio using Mac's built-in tools"""
    print("Listening for 5 seconds...")
    os.system("ffmpeg -f avfoundation -i ':0' -t 5 temp.wav -y 2>/dev/null")
    
    segments, _ = model_stt.transcribe("temp.wav")
    text = "".join([seg.text for seg in segments])
    return text

def speak(text):
    """Speak text output"""
    audio = model_tts.generate(text, voice="Hugo", speed=1)
    sf.write("output.wav", audio, 24000)
    os.system("afplay output.wav")
    print(f"Bot: {text}")

# Main
user_input = listen()
print(f"You: {user_input}")
speak(f"You said: {user_input}")