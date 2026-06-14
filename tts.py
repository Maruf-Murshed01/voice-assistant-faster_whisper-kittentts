from faster_whisper import WhisperModel
from kittentts import KittenTTS
import soundfile as sf
import os
import time

# Load models once at startup
print("Loading models...")
model_stt = WhisperModel("base")
model_tts = KittenTTS("KittenML/kitten-tts-mini-0.8")
print("✓ Models loaded!\n")

def listen():
    """Record audio using Mac's built-in tools"""
    print("Listening for 5 seconds...")
    os.system("ffmpeg -f avfoundation -i ':0' -t 5 temp.wav -y 2>/dev/null")
    
    try:
        segments, _ = model_stt.transcribe("temp.wav")
        text = "".join([seg.text for seg in segments]).strip()
        return text if text else None
    except Exception as e:
        print(f"Error transcribing: {e}")
        return None

def speak(text):
    """Speak text output"""
    try:
        audio = model_tts.generate(text, voice="Hugo", speed=1)
        sf.write("output.wav", audio, 24000)
        os.system("afplay output.wav")
        print(f"Bot: {text}\n")
    except Exception as e:
        print(f"Error speaking: {e}\n")

def get_response(user_input):
    """Simple chatbot logic"""
    user_lower = user_input.lower()
    
    # Simple responses
    if any(word in user_lower for word in ["hello", "hi", "hey"]):
        return "Hey! How can I help you today?"
    elif any(word in user_lower for word in ["how are you", "how do you feel"]):
        return "I'm doing great! Thanks for asking. How about you?"
    elif any(word in user_lower for word in ["what is your name", "who are you"]):
        return "I'm Kitten, your voice assistant!"
    elif any(word in user_lower for word in ["bye", "goodbye", "exit", "quit"]):
        return "Goodbye! See you soon!"
    elif any(word in user_lower for word in ["thank you", "thanks"]):
        return "You're welcome!"
    elif any(word in user_lower for word in ["time", "what time"]):
        from datetime import datetime
        return f"It's {datetime.now().strftime('%I:%M %p')}"
    else:
        return f"You said: {user_input}. That's interesting!"

# Main loop
print("=" * 50)
print("🐱 KITTEN VOICE ASSISTANT")
print("Say 'goodbye' to exit")
print("=" * 50 + "\n")

while True:
    try:
        user_input = listen()
        
        if not user_input:
            print("Sorry, didn't catch that. Try again.\n")
            continue
        
        print(f"You: {user_input}")
        
        # Check for exit
        if any(word in user_input.lower() for word in ["bye", "goodbye", "exit", "quit"]):
            speak("Goodbye!")
            print("Exiting...")
            break
        
        # Get and speak response
        response = get_response(user_input)
        speak(response)
        
    except KeyboardInterrupt:
        print("\n\nExiting...")
        break
    except Exception as e:
        print(f"Error: {e}\n")
        continue