from faster_whisper import WhisperModel
from kittentts import KittenTTS
import soundfile as sf
import os
import requests

# Initialize models
print("=" * 60)
print("🐱 Loading Kitten Voice Assistant...")
print("=" * 60)
model_stt = WhisperModel("base")
model_tts = KittenTTS("KittenML/kitten-tts-mini-0.8")
print("STT and TTS loaded")

# Check API key
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    print("\n ERROR: API_KEY not set!")
    exit(1)
print("API key found")

# Conversation history
conversation_history = []

def listen():
    """Record audio using Mac's built-in tools"""
    print("🎤 Listening for 5 seconds...")
    result = os.system("ffmpeg -f avfoundation -i ':0' -t 5 temp.wav -y 2>/dev/null")
    
    if result != 0:
        print("❌ Microphone error. Check permissions.")
        return None
    
    try:
        segments, _ = model_stt.transcribe("temp.wav")
        text = "".join([seg.text for seg in segments]).strip()
        return text if text else None
    except Exception as e:
        print(f"❌ Transcription error: {e}")
        return None

def speak(text):
    """Speak text output"""
    try:
        audio = model_tts.generate(text, voice="Hugo", speed=1)
        sf.write("output.wav", audio, 24000)
        os.system("afplay output.wav 2>/dev/null")
        print(f"🤖 Kitten: {text}\n")
    except Exception as e:
        print(f"❌ TTS error: {e}\n")

def get_groq_response(user_input):
    """Get response from Groq API"""
    try:
        # Add user message to history
        conversation_history.append({
            "role": "user",
            "content": user_input
        })
        
        # Prepare request
        headers = {
            "Authorization": f"Bearer {groq_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {
                    "role": "system",
                    "content": "You are Kitten, a friendly voice assistant. Keep responses short (1-3 sentences) and conversational."
                }
            ] + conversation_history,
            "max_tokens": 150,
            "temperature": 0.7
        }
        
        # Make request
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            json=payload,
            headers=headers,
            timeout=10
        )
        
        # Handle errors
        if response.status_code != 200:
            error_msg = response.json().get('error', {}).get('message', 'Unknown error')
            print(f"API error: {error_msg}")
            return None
        
        # Extract response
        response_text = response.json()["choices"][0]["message"]["content"]
        
        # Add to history
        conversation_history.append({
            "role": "assistant",
            "content": response_text
        })
        
        return response_text
        
  
    except Exception as e:
        print(f"Error: {e}")
        return None

# Main loop
print("=" * 60)
print("🐱 KITTEN VOICE ASSISTANT")
print("Made by Maruf")
print("=" * 60)
print("Say 'goodbye' to exit\n")

turn = 0

while True:
    try:
        turn += 1
        
        user_input = listen()
        
        if not user_input:
            print("Didn't catch that. Try again.\n")
            continue
        
        print(f"👤 You: {user_input}")
        
        # Check for exit
        if any(word in user_input.lower() for word in ["bye", "goodbye", "exit", "quit"]):
            speak("Goodbye! It was nice talking to you.")
            print("\n" + "=" * 60)
            print(f"Thanks for {turn} conversations! See you later! 👋")
            print("=" * 60)
            break
        
        # Get response
        print("🤔 Thinking...")
        response = get_groq_response(user_input)
        
        if response:
            speak(response)
        else:
            print("⚠️  Couldn't generate response. Try again.\n")
        
    except KeyboardInterrupt:
        print("\n\n" + "=" * 60)
        print("Exiting... Thanks for using Kitten! 👋")
        print("=" * 60)
        break
    except Exception as e:
        print(f"❌ Unexpected error: {e}\n")
        continue