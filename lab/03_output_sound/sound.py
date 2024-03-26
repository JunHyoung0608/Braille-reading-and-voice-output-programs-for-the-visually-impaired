from gtts import gTTS
textfile = "./texts/text0.txt"
save_mp3 = "./sound/sound.mp3"
language = "ko"

def trans_mp3(textfile,language,ss=False):
    sp = gTTS(
        text=textfile,
        lang=language,
        slow=ss
    )
    sp.save(save_mp3)



if __name__ == "__main__":
    trans_mp3(textfile,language)