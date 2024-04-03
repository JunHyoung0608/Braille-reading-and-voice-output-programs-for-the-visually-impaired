from gtts import gTTS
import playsound                                    #pip install playsound==1.2.2
import os.path
from os import path
text_file = "./texts/text3.txt"
save_mp3 = "./sound/sound.mp3"
language = "ko"

def trans_mp3(text_file, save_mp3, language, ss=False):         #text_file : 텍스트 파일명, language : 변역국어, ss : 슬로우모드
    with open(text_file, "r", encoding='utf-8') as f:
        text_line = f.readline()

    sp = gTTS(                                                  #텍스트를 음성변환
        text=text_line,
        lang=language,
        slow=ss
    )
    sp.save(save_mp3)
        

    if path.exists(save_mp3):                                   #지정된 주소의 mp3 파일이 존재 여부 확인 시 재생
        playsound.playsound(save_mp3)



if __name__ == "__main__":
    trans_mp3(text_file, save_mp3,language)