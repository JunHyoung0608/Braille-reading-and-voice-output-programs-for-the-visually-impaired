from gtts import gTTS
import playsound

text = ""

file_name = ".mp3"

tts = gTTS(text=text, lang="ko")

tts.save(file_name)

playsound.playsound(file_name)