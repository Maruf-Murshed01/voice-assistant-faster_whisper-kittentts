from kittentts import KittenTTS
import soundfile as sf

model = KittenTTS("KittenML/kitten-tts-mini-0.8")
audio = model.generate("Hey Maruf, whats up, are you okay, it seems you are working on a TTS, its a very amazing tool, start slowly and you will observe it, This is your first tts project and you are doing awesome and its very interesting that you are working on this kind of project, it shows your determi... and hardwork(smile) beyond your worklife", voice="Bella", speed=5.5)
sf.write("output.wav", audio, 24000)
print("Done! Check output.wav")
