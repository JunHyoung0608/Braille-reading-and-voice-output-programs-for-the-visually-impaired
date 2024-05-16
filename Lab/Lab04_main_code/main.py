#00~03까지의 내용을 합성한다.
import cv2 as cv
from gtts import gTTS
import playsound        #pip install playsound==1.2.2
import os.path
from os import path
import torch
import pandas as pd

save_imgfile = "./img/camera_img.PNG"

def capture(width, height):
    
    cap = cv.VideoCapture(0)                        
    cap.set(cv.CAP_PROP_FRAME_WIDTH, width)         
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, height)       
    #cap.set(cv.CAP_PROP_AUTO_EXPOSURE, 0)           # 자동 노출 비활성화
    #cap.set(cv.CAP_PROP_EXPOSURE, 1.0)              # 노출 조절 (0.0 ~ 1.0)
    #cap.set(cv.CAP_PROP_BRIGHTNESS, 1.0)


    if not cap.isOpened():                              
        print("Error CAM : Camera connection filed")
        exit()
    else:
        ret, img = cap.read()                       
        if not ret:                                 
            print("Error CAM : Can't read the camera data")
            return None
                
    cap.release()                                   
    return img

def img_post_processing(img,path='./data/post_img'):
    # 이미지 읽기
    img = cv.imread(img)

    # 이미지를 640x640으로 리사이즈
    resized_img = cv.resize(img, (640, 640))

    # 그레이스케일로 변환
    grayscale_img = cv.cvtColor(resized_img, cv.COLOR_BGR2GRAY)

    equalized_img = cv.equalizeHist(grayscale_img)

    save_file = 'post_img0.jpg'
    for file in path:
        if file == save_file:
            save_file = save_file[:-5] + str(int(save_file[-5])+1) + save_file[-4:]


    post_path = path + '/' + save_file
    cv.imwrite(post_path, equalized_img)

    return equalized_img

def yolo_detect(input_img, img_size=640):
    output_dir = './data/output/'

    model = torch.hub.load('../Lab01_Object_Dection/yolov5', 'custom', path='./data/weights/best.pt', source='local')

    model.max_det = 64  # 객체 탐지 수
    model.conf = 0.4  # 신뢰도 값
    model.multi_label = True   # 라벨링이 여러개가 가능하도록 할지
    model.iou = 0.5  # 0.4 ~ 0.5 값

    result = model(input_img, size = img_size) #이미지와 size를 넣어 결과를 얻어낸다

    result.print() # 모델 적용 후 결과 출력
    result.save(save_dir=output_dir,exist_ok=True)  # 결과사진을 저장
    result.xyxy[0]
    result.pandas().xyxy[0]
    return result.pandas().xyxy[0]

def sort_data(xyxy):
    x_lst = (xyxy['xmax'] - xyxy['xmin'])/2 + xyxy['xmin']
    xyxy['x'] = x_lst
    y_lst = (xyxy['ymax'] - xyxy['ymin'])/2 + xyxy['ymin']
    xyxy['y'] = y_lst

    xyxy_rev = xyxy.sort_values('ymax')
    xyxy_rev = xyxy_rev.reset_index()
    x_mean = sum(xyxy_rev['xmax'] - xyxy_rev['xmin'])/len(xyxy_rev['xmax'])
    y_mean = sum(xyxy_rev['ymax'] - xyxy_rev['ymin'])/len(xyxy_rev['ymax'])
    x_lst = xyxy

    #y line 
    index = []
    y_limt = (xyxy_rev['y'][0] + (y_mean * 0.9))
    for i,y in enumerate(xyxy_rev['y']):
        if y >= y_limt:
            index.append(i)
            y_limt = y + (y_mean * 0.9)
    
    #한줄일경우
    if (index == []):
        index.append(len(xyxy_rev) - 1)
    



    #x line
    line = []
    data_lst = [0]
    for i in index:
        line = []
        line = pd.DataFrame(line, columns = ['x', 'name', 'confidence', 'xmax', 'xmin'])
        line['x'] = xyxy_rev['x'][0:i]
        line['xmax'] = xyxy_rev['xmax'][0:i]
        line['xmin'] = xyxy_rev['xmin'][0:i]
        line['name'] = xyxy_rev['name'][0:i]
        line['confidence'] = xyxy_rev['confidence'][0:i]
        line_sort = line.sort_values('x')
        line_sort = line_sort.reset_index()

        x_limt = (line_sort['x'][0] + (x_mean * 1.5))
        for i,x in enumerate(line_sort['x']):
            if( i != len(line_sort['x'])-1):
                if(line_sort['x'][i+1] - line_sort['x'][i] >= (x_mean * 0.2)):
                    if x >= x_limt:
                        data_lst.append(0)
                    data_lst.append(int(line_sort['name'][i]))
                    x_limt = (x + (x_mean * 1.5))
        data_lst.append(0)
    return data_lst

def check_kind(index,data):
    #               ㄱ         ㄴ          ㄷ          ㄹ          ㅁ          ㅂ          ㅅ          ㅈ           ㅊ          ㅋ          ㅌ          ㅍ          ㅎ
    INITIAL_LIST = {8: 0x1100, 9: 0x1102, 10: 0x1103, 16: 0x1105, 17: 0x1106, 24: 0x1107, 32: 0x1109, 40: 0x110C, 48: 0x110E, 11: 0x110F, 19: 0x1110, 25: 0x1111, 26: 0x1112}
    #                  ㅏ           ㅑ          ㅓ          ㅕ          ㅗ          ㅛ          ㅜ          ㅠ          ㅡ           ㅣ          ㅐ          ㅒ            ㅔ        ㅖorㅐ     ㅘorㅙ      ㅚ          ㅝorㅞ       ㅟ     ㅢ
    NEUTRALITY_LIST = {35: 0x1161, 28: 0x1163, 14: 0x1165, 49: 0x1167, 37: 0x1169, 44: 0x116D, 13: 0x116E, 41: 0x1172, 42: 0x1173, 21: 0x1175, 23: 0x1162, 28: 0x1162, 29:0x1166, 36:0x116A, 39: 0x116A, 61: 0x116C, 15: 0x116F, 13:0x1171,58: 0x1164}
    #            ㄱ         ㄴ          ㄷ          ㄹ          ㅁ          ㅂ          ㅅ         ㅇ         ㅈ         ㅊ          ㅋ          ㅌ          ㅍ          ㅎ           ㅆ             
    FINAL_LIST = {1: 0x11A8, 18: 0x11AB, 20: 0x11AE, 2: 0x11AF, 34: 0x11B7, 3: 0x11B8, 4: 0x11BA, 54: 0x11BC, 5: 0x11BD, 6: 0x11BE, 22: 0x11BF, 38: 0x11B0, 50: 0x11B1, 52: 0x11B2, 12: 0x11BB}
    AND_LIST = {14:[0x1100,0x1173,0x1105,0x1162,0x1109,0x1165], 
                9:[0x1100,0x1173,0x1105,0x1165,0x1102,0x1161], 
                18:[0x1100,0x1173,0x1105,0x1165,0x1106,0x1167,0x11AB], 
                34:[0x1100,0x1173,0x1105,0x1165,0x1106,0x1173,0x1105,0x1169], 
                29:[0x1100,0x1173,0x1105,0x1165,0x11AB,0x1103,0x1166], 
                37:[0x1100,0x1173,0x1105,0x1175,0x1100,0x1169], 
                49:[0x1100,0x1173,0x1105,0x1175,0x1112,0x1161,0x110B,0x1167]}
    NUM_LIST = {1: '1', 3: '2', 9: '3', 25: '4', 17: '5', 11: '6', 27: '7', 19: '8', 10: '9', 26: '0'}
    #               가            나        다          마          바          사           자          카          타          파          하
    SHORT_LIST_BE = {43: 0x1100, 9: 0x1102, 10: 0x1103, 17: 0x1106, 24: 0x1107, 7: 0x1109, 40: 0x110C, 11: 0x110F, 19: 0x1110, 25: 0x1111, 26: 0x1112}
    #               억                    언                    얼                  연                  열                  영                  옥                  옥                  온                  옹                  울                  은                  을                  인                  것         
    SHORT_LIST_AF = {57: [0x1165,0x11A8], 62:[0x1165,0x11AB], 30:[0x1165,0x11AF], 33:[0x1167,0x11AB], 51:[0x1167,0x11AF], 59:[0x1167,0x11BC], 45:[0x1169,0x11A8], 55:[0x1169,0x11AB], 63:[0x1169,0x11BC], 27:[0x116E,0x11AB], 47:[0x116E,0x11AF], 53:[0x1173,0x11AB], 46:[0x1173,0x11AF], 31:[0x1175,0x11AB], 56:[0x1100,0x1165,0x11BA]}
    #BUHO_LIST = {25:'.',38:'?',22:'!',16:',',36:'-',38:'"',52:'"'}
    # 36,36 => '~', 20,20 => '*', 32,38:''',52,4:''',16,2:':',48,6:';',32,32,32: ...
    NUM = 60; STRONG = 32
    result = []                                                                    

    #숫자                                                                                                                                    
    if data[index] == NUM:                                                                        
        while data[index+1] != 0:
            index += 1; key = data[index]
            result.append(NUM_LIST[key])
    #약어                                                                                                                                                               
    elif (data[index] == 1) and (data[index-1] == 0) and (data[index+1] in AND_LIST):
        key = data[index+1]
        result += AND_LIST[key]
        index += 1
    #약자-AF                                                                                                                                                                  
    elif (data[index] in SHORT_LIST_AF): 
        key = data[index]
        if (data[index-1] not in INITIAL_LIST) or (data[index-1] == 0): # 첫글자 모음 시 ㅇ추가 
            result.append(0x110B)
        result += SHORT_LIST_AF[key]
    #약자-BE
    elif (data[index] in SHORT_LIST_BE) and ((data[index+1] in INITIAL_LIST) or (data[index+1] in SHORT_LIST_BE) or (data[index+1] == 0) or (data[index+1] == NUM) or (data[index+1] in FINAL_LIST)):
        key = data[index]
        result.append(SHORT_LIST_BE[key]); result.append(0x1161)   #reuslt <=== [value,0x1161(ㅏ)]
    #초성-된소리                                                                                                                                                       
    elif (data[index] == STRONG) and (data[index+1] in INITIAL_LIST):                                                                                                                                                              
        key = data[index+1]
        result.append(INITIAL_LIST[key]+1)
        if(data[index+2] not in NEUTRALITY_LIST) or(data[index+2] not in SHORT_LIST_AF):
            result.append(0x1161)
        index += 1
    #초성
    elif data[index] in INITIAL_LIST:
        key = data[index]
        result.append(INITIAL_LIST[key])
        # if(data[index+1] not in NEUTRALITY_LIST) or(data[index+1] not in SHORT_LIST_AF):
        #     result.append(0x1161)
    #중성 
    elif data[index] in NEUTRALITY_LIST:                                                                                                                                                                                                                                          
        key = data[index]
        if (data[index-1] not in INITIAL_LIST) or (data[index-1] == 0):
            result.append(0x110B)
        if data[index] == 36:
            if data[index+1] == 23:         #ㅐ
                result.append(0x1162)
            elif data[index+1] == 12:       #ㅖ
                result.append(0x1168)
            index += 1
        elif data [index] == 39:
            if data[index+1] == 23:         #ㅙ
                result.append(0x1162)
                index += 1
            else:
                result.append(0x116A)       #ㅘ
        elif data[index] == 15:
            if data[index+1] == 23:         #ㅞ
                result.append(0x1170)
                index += 1
            else:
                result.append(0x116F)       #ㅝ
        elif data[index] == 13:
            if data[index+1] == 23:
                result.append(0x1171)       #ㅟ
                index += 1
            else:
                result.append(0x116E)       #ㅜ
        else:
            result.append(NEUTRALITY_LIST[key])
    #종성-곁받침
    elif (data[index] in FINAL_LIST) and (data[index+1] in FINAL_LIST):
        if data[index] == 1:
            if data[index+1] == 1:      #ㄲ
                result.append(0x11A9)
            elif data[index+1] == 4:    #ㄳ
                result.append(0x11AA)
        elif data[index] == 18:
            if data[index+1] == 5:      #ㄵ
                result.append(0x11AC)
            elif data[index+1] == 52:   #ㄶ
                result.append(0x11AD)
        elif data[index] == 2:
            if data[index+1] == 1:      #ㄺ
                result.append(0x11B0)
            elif data[index+1] == 34:   #ㄻ
                result.append(0x11B1)
            elif data[index+1] == 3:    #ㄼ
                result.append(0x11B2)
            elif data[index+1] == 4:    #ㄽ
                result.append(0x11B3)
            elif data[index+1] == 38:   #ㄾ
                result.append(0x11B4)
            elif data[index+1] == 50:   #ㄿ
                result.append(0x11B5)
            elif data[index+1] == 52:   #ㅀ
                result.append(0x11B6)
        elif data[index] == 3:
            if data[index+1] == 4:      #ㅄ
                result.append(0x11B9)
        index += 1
    #종성
    elif data[index] in FINAL_LIST:                                                                                                                                 
        key = data[index]
        result.append(FINAL_LIST[key])
    #띄어쓰기
    elif data[index] == 0:                                                                                                                                         
        result.append(' ')
    #온점
    elif data[index] == 25:
        result.append('.')

    return index+1, result


def trans_data(input_data):
    print('input\t','index\t','value\t\t','kind',)
    index = 0
    uni = []
    uni_lst = []
    txt=''
    
    while len(input_data) > index:
        print(input_data[index],end=' ')

        index, uni = check_kind(index,input_data)
        
        
        uni_lst += uni
        print('\t',index+1,'\t',uni,'\t',end='')
        for i in uni :
            if type(i) == type(1):
                print(chr(i),end='')
            else:
                print(i)
        print('')

    for i in uni_lst:
        if type(i) == type(1):
            txt += chr(i)
        else:
            txt += i

    for i,data in enumerate(txt):
        if (data >= chr(0x1100)) and (data <= chr(0x1112)):
            if (txt[i+1] < chr(0x1161)) or (txt[i+1] > chr(0x1175)):
                txt = txt[0:i+1] + chr(0x1175) + txt[i+1:]
    return txt


def trans_mp3(text_file, save_mp3, language="ko", ss=False):         
    with open(text_file, "r", encoding='utf-8') as f:
        text_line = f.readline()

    sp = gTTS(                                                  
        text=text_line,
        lang=language,
        slow=ss
    )
    for file in save_mp3[:7]:
        if file == save_mp3[8:]:
            save_mp3 = save_mp3[:-5] + str(int(save_mp3[-5])+1) + save_mp3[-4:]
    
    sp.save(save_mp3)
        

    if path.exists(save_mp3):                                   
        playsound.playsound(save_mp3)



def main(img):
    img_p = img_post_processing(img)

    #추론
    xyxy = yolo_detect(img_p)
    data_lst = sort_data(xyxy)

    #점자해석
    result = trans_data(data_lst)
    
    if result == '':
        result = '점자가 인식된게 없습니다. 다시 찍어주세요'
    #사운드출력
    trans_mp3(result,save_mp3 = "./data/sound/sound0.mp3")

if __name__ == '__main__':
    #카메라 입력
    img = capture(640, 480)
    if img is not None:
        cv.imshow('Camera_image', img)
        main(img)
        cv.waitKey(0)
        cv.destroyAllWindows()
    else :
        print("error : Don't have image file" )

