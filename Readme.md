# Kitten Voice Assistant

A lightweight, local voice assistant for macOS. Speak into your microphone, and Kitten listens, understands what you said, and replies out loud.

Everything runs on your machine — no cloud APIs, no API keys, no internet required after setup.

---

## What it does

1. **Listens** — records 5 seconds of audio from your microphone
2. **Understands** — transcribes your speech to text using [faster-whisper](https://github.com/SYSTRAN/faster-whisper)
3. **Responds** — picks a reply based on simple keyword matching
4. **Speaks** — converts the reply to speech using [KittenTTS](https://github.com/KittenML/KittenTTS) and plays it through your speakers

Say **"goodbye"**, **"bye"**, **"exit"**, or **"quit"** to end the session. Press `Ctrl+C` to stop at any time.

---

## Requirements

| Requirement | Notes |
|-------------|-------|
| **macOS** | Uses `ffmpeg` (avfoundation) for recording and `afplay` for playback |
| **Python 3.12** | Tested with 3.12 |
| **ffmpeg** | Install with `brew install ffmpeg` if not already installed |
| **Microphone** | Terminal (or your IDE) needs microphone permission in System Settings |

---

## Quick start

### 1. Clone and enter the project

```bash
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
pip install soundfile faster-whisper
```

### 4. Run the assistant

```bash
python tts.py
```

On first launch, models are downloaded and loaded. This can take a minute. After that, you should see:

```
==================================================
🐱 KITTEN VOICE ASSISTANT
Say 'goodbye' to exit
==================================================

Listening for 5 seconds...
```

Speak clearly after you see **"Listening for 5 seconds..."**.

---

## Example conversation

```
Listening for 5 seconds...
You: hello
Bot: Hey! How can I help you today?

Listening for 5 seconds...
You: what is your name
Bot: I'm Kitten, your voice assistant!

Listening for 5 seconds...
You: goodbye
Bot: Goodbye!
Exiting...
```

---

## Supported commands

The assistant uses simple keyword matching. It understands phrases like:

| You can say… | Kitten replies… |
|--------------|-----------------|
| hello, hi, hey | A friendly greeting |
| how are you | A short check-in response |
| what is your name, who are you | Introduces itself as Kitten |
| thank you, thanks | You're welcome |
| what time, time | Current local time |
| goodbye, bye, exit, quit | Says goodbye and exits |
| Anything else | Echoes what you said |

To add more responses, edit the `get_response()` function in `tts.py`.

---

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
get_response() (keyword matching)
    │
    ▼
KittenTTS (text → audio)
    │
    ▼
afplay (play output.wav)
```

### Key files

| File | Purpose |
|------|---------|
| `tts.py` | Main application — listen, transcribe, respond, speak |
| `temp.wav` | Temporary recording from your microphone (created each turn) |
| `output.wav` | Generated speech output (created each reply) |

Both `.wav` files are written to the directory you run the script from.

---

## Customization

### Change the voice

KittenTTS ships with eight voices. Open `tts.py` and change the `voice` argument in `speak()`:

```python
audio = model_tts.generate(text, voice="Hugo", speed=1)
```

Available voices: **Bella**, **Jasper**, **Luna**, **Bruno**, **Rosie**, **Hugo**, **Kiki**, **Leo**

### Adjust speech speed

```python
audio = model_tts.generate(text, voice="Hugo", speed=1.5)  # faster
audio = model_tts.generate(text, voice="Hugo", speed=0.8)  # slower
```

### Change recording duration

In `listen()`, update the `-t` flag in the ffmpeg command:

```python
os.system("ffmpeg -f avfoundation -i ':0' -t 5 temp.wav -y 2>/dev/null")
#                                              ^ seconds
```

---

## Troubleshooting

### No audio / can't hear the bot

- Check your Mac **volume** and output device (headphones vs speakers).
- Confirm `output.wav` was created in the project folder after a reply.
- Test playback manually:
  ```bash
  afplay output.wav
  ```
- Make sure you run the script from the project directory so relative paths resolve correctly.

### "Sorry, didn't catch that"

- Speak right after **"Listening for 5 seconds..."** appears.
- Move closer to the microphone and reduce background noise.
- Grant **microphone access** to Terminal or your IDE:  
  **System Settings → Privacy & Security → Microphone**

### `ffmpeg: command not found`

Install ffmpeg:

```bash
brew install ffmpeg
```

### Wrong microphone is being used

List available audio devices:

```bash
ffmpeg -f avfoundation -list_devices true -i ""
```

Then update the device index in `tts.py` (e.g. `':1'` instead of `':0'`).

### Models take a long time to load

This is normal on first run. Whisper and KittenTTS models are downloaded and cached locally. Later runs are faster.

---

## Tech stack

| Layer | Tool |
|-------|------|
| Speech-to-text | [faster-whisper](https://github.com/SYSTRAN/faster-whisper) (Whisper `base` model) |
| Text-to-speech | [KittenTTS](https://github.com/KittenML/KittenTTS) (`kitten-tts-mini-0.8`) |
| Audio I/O | `ffmpeg`, `afplay`, `soundfile` |
| Language | Python 3.12 |

---

## Project structure

```
kitten/
├── tts.py          # Voice assistant application
├── Readme.md       # This file
├── .gitignore
├── temp.wav        # Generated at runtime (mic recording)
└── output.wav      # Generated at runtime (TTS output)
```

---

## Roadmap ideas

- [ ] Conversation loop with configurable wake word
- [ ] LLM-powered responses instead of keyword matching
- [ ] Cross-platform support (Linux / Windows)
- [ ] Config file for voice, speed, and recording duration

---

## Acknowledgements

- [KittenML / KittenTTS](https://github.com/KittenML/KittenTTS) for lightweight on-device text-to-speech
- [SYSTRAN / faster-whisper](https://github.com/SYSTRAN/faster-whisper) for efficient speech recognition
