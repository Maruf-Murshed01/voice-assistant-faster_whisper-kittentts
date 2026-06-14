# Kitten Voice Assistant

A lightweight voice assistant for macOS. Speak into your microphone — Kitten transcribes your speech locally, generates a conversational reply via [Groq](https://groq.com), and speaks the answer back using on-device text-to-speech.

## Features

- **Local speech-to-text** — [faster-whisper](https://github.com/SYSTRAN/faster-whisper) transcribes audio on your machine
- **LLM-powered replies** — Groq (`llama-3.1-8b-instant`) with short, conversational responses
- **Local text-to-speech** — [KittenTTS](https://github.com/KittenML/KittenTTS) synthesizes speech without a cloud TTS API
- **Conversation memory** — maintains context across turns within a session
- **Hands-free loop** — continuous listen → think → speak until you say goodbye

## Requirements

| Requirement | Notes |
|-------------|-------|
| **macOS** | Uses `ffmpeg` (avfoundation) for recording and `afplay` for playback |
| **Python 3.12** | Tested with 3.12 |
| **ffmpeg** | `brew install ffmpeg` |
| **Groq API key** | Free tier available at [console.groq.com](https://console.groq.com) |
| **Microphone** | Grant access to Terminal or your IDE in System Settings |

## Quick start

### 1. Clone and enter the project

```bash
git clone <your-repo-url>
cd kitten
```

### 2. Create a virtual environment

```bash
python3.12 -m venv tts_env
source tts_env/bin/activate
```

### 3. Install dependencies

```bash
pip install https://github.com/KittenML/KittenTTS/releases/download/0.8.1/kittentts-0.8.1-py3-none-any.whl
pip install soundfile faster-whisper requests
```

### 4. Set your Groq API key

```bash
export GROQ_API_KEY="your-api-key-here"
```

### 5. Run

```bash
python tts.py
```

On first launch, Whisper and KittenTTS models are downloaded and cached locally. This can take a minute.

```
============================================================
🐱 KITTEN VOICE ASSISTANT
Say 'goodbye' to exit
============================================================

🎤 Listening for 5 seconds...
```

Speak after **"Listening for 5 seconds..."** appears. Say **goodbye**, **bye**, **exit**, or **quit** to end the session. Press `Ctrl+C` to stop at any time.

## Example session

```
🎤 Listening for 5 seconds...
👤 You: hello
🤔 Thinking...
🤖 Kitten: Hey! How can I help you today?

🎤 Listening for 5 seconds...
👤 You: what's the capital of France?
🤔 Thinking...
🤖 Kitten: The capital of France is Paris!

🎤 Listening for 5 seconds...
👤 You: goodbye
🤖 Kitten: Goodbye! It was nice talking to you.
```

## How it works

```
Microphone
    │
    ▼
ffmpeg (record 5s → temp.wav)
    │
    ▼
faster-whisper (speech → text)
    │
    ▼
Groq API (LLM reply + conversation history)
    │
    ▼
KittenTTS (text → audio)
    │
    ▼
afplay (play output.wav)
```

| File | Purpose |
|------|---------|
| `tts.py` | Main application |
| `temp.wav` | Microphone recording (created each turn) |
| `output.wav` | Generated speech (created each reply) |

## Configuration

### Voice and speed

In `tts.py`, edit the `speak()` call:

```python
audio = model_tts.generate(text, voice="Hugo", speed=1)
```

Voices: **Bella**, **Jasper**, **Luna**, **Bruno**, **Rosie**, **Hugo**, **Kiki**, **Leo**

### Recording duration

In `listen()`, change the `-t` flag:

```python
os.system("ffmpeg -f avfoundation -i ':0' -t 5 temp.wav -y 2>/dev/null")
#                                              ^ seconds
```

### LLM model and system prompt

Adjust `model`, `max_tokens`, `temperature`, or the system message in `get_groq_response()` inside `tts.py`.

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `ERROR: API_KEY not set!` | Export `GROQ_API_KEY` before running |
| No audio from the bot | Check volume/output device; run `afplay output.wav` |
| "Didn't catch that" | Speak right after the listening prompt; reduce background noise |
| Microphone not working | **System Settings → Privacy & Security → Microphone** |
| `ffmpeg: command not found` | `brew install ffmpeg` |
| Wrong microphone | List devices with `ffmpeg -f avfoundation -list_devices true -i ""`, then update `':0'` in `tts.py` |
| Slow first startup | Normal — models download once and are cached locally |

## Tech stack

| Layer | Tool |
|-------|------|
| Speech-to-text | [faster-whisper](https://github.com/SYSTRAN/faster-whisper) (Whisper `base`) |
| Language model | [Groq](https://groq.com) — `llama-3.1-8b-instant` |
| Text-to-speech | [KittenTTS](https://github.com/KittenML/KittenTTS) (`kitten-tts-mini-0.8`) |
| Audio I/O | `ffmpeg`, `afplay`, `soundfile` |

## Project structure

```
kitten/
├── tts.py       # Voice assistant application
├── Readme.md
├── .gitignore
├── temp.wav     # Runtime (gitignored)
└── output.wav   # Runtime (gitignored)
```

## Acknowledgements

- [KittenML / KittenTTS](https://github.com/KittenML/KittenTTS) — on-device text-to-speech
- [SYSTRAN / faster-whisper](https://github.com/SYSTRAN/faster-whisper) — efficient speech recognition
- [Groq](https://groq.com) — fast LLM inference
