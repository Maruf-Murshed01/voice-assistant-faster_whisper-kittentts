# KittenTTS Simple App

A lightweight text-to-speech application using KittenTTS.

## Setup

```bash
python3.12 -m venv tts_env
source tts_env/bin/activate
pip install https://github.com/KittenML/KittenTTS/releases/download/0.8.1/kittentts-0.8.1-py3-none-any.whl
pip install soundfile
```

## Usage

```python
from kittentts import KittenTTS
import soundfile as sf

model = KittenTTS("KittenML/kitten-tts-mini-0.8")
audio = model.generate("Hello world!", voice="Bella")
sf.write("output.wav", audio, 24000)
```

## Available Voices

Bella, Jasper, Luna, Bruno, Rosie, Hugo, Kiki, Leo

## Speed Control

```python
model.generate("Hello", voice="Bella", speed=1.5)  # Faster
model.generate("Hello", voice="Luna", speed=0.8)   # Slower
```



Run 

python [tts.py](http://tts.py)



Done! 🐱



