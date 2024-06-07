import cv2 as cv
from gtts import gTTS
import playsound        #pip install playsound==1.2.2
import os.path
from os import path
import torch
import pandas as pd
import numpy as np

def save_file(input_img,f_name,f_extension,path):
    i = 0
    for file in os.listdir(path):
        if file == f_name+str(i)+'.'+f_extension:
            i += 1
        else:
            break


    input_path = path + '/' + f_name + f_name+str(i)+f_extension
    cv.imwrite(input_path, input_img)

def img_post_processing(img,path='./data/post_img'):
    # 이미지 읽기
    # 이미지를 640x640으로 리사이즈
    resized_img = cv.resize(img, (720, 720))

    # 그레이스케일로 변환
    grayscale_img = cv.cvtColor(resized_img, cv.COLOR_BGR2GRAY)

    save_file(grayscale_img,'post_img','jpg','./data/post_img')

    return grayscale_img

def yolo_detect(input_img, img_size=720):
    output_dir = './data/output/'

    model = torch.hub.load('../Lab01_Object_Dection/yolov5', 'custom', path='./data/weights/best.pt', source='local')

    model.max_det = 64  # 객체 탐지 수
    model.conf = 0.50  # 신뢰도 값
    model.multi_label = False   # 라벨링이 여러개가 가능하도록 할지
    model.iou = 0.4  # 0.4 ~ 0.5 값

    result = model(input_img, size = img_size) #이미지와 size를 넣어 결과를 얻어낸다

    result.print() # 모델 적용 후 결과 출력
    result.save(save_dir=output_dir,exist_ok=True)  # 결과사진을 저장
    result.xyxy[0]
    result.pandas().xyxy[0]
    return result.pandas().xyxy[0]

    
def is_circle_approx(image, value=0.5):
    # 이미지 윤곽선을 찾습니다
    contours, _ = cv.findContours(image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        # 모양의 윤곽선을 찾습니다
        area = cv.contourArea(contour)
        if (area < 600):
            continue
        
        # 윤곽선의 외접 원을 찾습니다
        (x, y), radius = cv.minEnclosingCircle(contour)
        circle_area = np.pi * (radius ** 2)

        # 원형성 비율을 계산합니다 (원에 가까울수록 1에 가까움)
        circularity = area / circle_area
        
        # 원형성 비율이 일정 임계값(예: 0.85) 이상이면 원으로 간주합니다
        print('circularity',circularity,'\tarea',area)
        if circularity > value:
            return 1
    
    return 0

def heck_one_bralie(img_cut,num_value_rev):

    height, width = img_cut.shape[:2]
    
    #바운딩 박스 크기 고정화
    img_cut = cv.resize(img_cut, (int(300*(width/height)) ,300))
    height, width = img_cut.shape[:2]


    #점자를 이미지를 2x3으로 자름-------------------------------------------
    cropped_images = [
        img_cut[:height//3, :width//2],               # 1번 부분
        img_cut[height//3:2*height//3, :width//2],    # 2번 부분
        img_cut[2*height//3:, :width//2],             # 3번 부분
        img_cut[:height//3, width//2:],               # 4번 부분
        img_cut[height//3:2*height//3, width//2:],    # 5번 부분
        img_cut[2*height//3:, width//2:]              # 6번 부분
    ]
        
    # 픽셀 값이 0인 경우를 방지하기 위해 작은 값을 더함
    img_a = img_cut + 1e-10
            
    # 조화 평균 밝기 계산
    harmonic_mean_brightness = len(img_a.flatten()) / np.sum(1.0 / img_a)
    num_value = 0
    means = []
    for cropped_image in cropped_images:
        means.append(np.mean(cropped_image))
    h_mean = sum(means) / len(cropped_images)
    num_value = harmonic_mean_brightness+(h_mean-harmonic_mean_brightness)*4
    print('-------------------')
    
    if (num_value < harmonic_mean_brightness*1.2) or (num_value > num_value_rev * 1.25):
        print('Updata')
        num_value = num_value_rev

    num_value_rev = num_value
    
    bralie = 0
    # 자른 이미지를 순회하며 화면에 표시
    for i, cropped_image in enumerate(cropped_images):

        #산술 평균 밝기 계산
        mean = np.mean(cropped_image)
        #이진화
        _, dst = cv.threshold(cropped_image, num_value, 255, cv.THRESH_BINARY)
        check = is_circle_approx(dst,0.4)
        bralie += check << i
    
            
        cv.imshow(f"A{i+1}", cropped_image)
        cv.imshow(f"C{i+1}", dst) 
    cv.waitKey(0)
    print('bralie',bin(bralie))
    return bralie,num_value

def check_all_bralies(img,data_a):
    #소벨-------------------------------------------------------------------
    Fx = np.array([[-1,0,1],
                   [-2,0,2],
                   [-1,0,1]])
    
    Fy = np.array([[1,2,1],
                   [0,0,0],
                   [-1,-2,-1]])

    edge_x = cv.filter2D(img, cv.CV_64F, Fx)
    edge_y = cv.filter2D(img, cv.CV_64F, Fy)

    sobel = cv.magnitude(edge_x, edge_y)
    sobel = np.clip(sobel, 0 ,255).astype(np.uint8)
    #블러처리--------------------------------------------------------------
    blur_image = cv.medianBlur(sobel, 5)
    #모든 점자 확인--------------------------------------------------
    bralie_lst = [0]
    num_value_rev = 300
    print('data_in',data_a)
    for i in range(len(data_a)):
        print(i,data_a['x'][i])
        cv.rectangle(img, (int(data_a['xmin'][i]), int(data_a['ymin'][i])), (int(data_a['xmax'][i]), int(data_a['ymax'][i])), (0, 255, 0), 2)
        #좌측 상단 부터 차례로 읽기
        img_cut = blur_image[int(data_a['ymin'][i]):int(data_a['ymax'][i]), int(data_a['xmin'][i]):int(data_a['xmax'][i])]
        
        bralie,num_value_rev = heck_one_bralie(img_cut,num_value_rev)
        bralie_lst.append(bralie)
        cv.imshow('Image with Rectangle', img)  # 결과 이미지를 화면에 표시합니다.
        cv.waitKey(0)  # 키 입력을 기다립니다.
    bralie_lst.append(0)

    return bralie_lst


def sort_data(xyxy, img):
    #바운딩 박스의 중심xy 계산
    center_x_lst = (xyxy['xmax'] - xyxy['xmin'])/2 + xyxy['xmin']
    xyxy['x'] = center_x_lst
    center_y_lst = (xyxy['ymax'] - xyxy['ymin'])/2 + xyxy['ymin']
    xyxy['y'] = center_y_lst

    #y에 대해 정렬
    xyxy_sort_y = xyxy.sort_values('ymax')
    xyxy_sort_y = xyxy_sort_y.reset_index()

    #평균 박스의 크기 구하기
    box_width_mean = sum(xyxy_sort_y['xmax'] - xyxy_sort_y['xmin'])/len(xyxy_sort_y['xmax'])
    box_height_mean = sum(xyxy_sort_y['ymax'] - xyxy_sort_y['ymin'])/len(xyxy_sort_y['ymax'])
    

    
    #문장의 행 구분
    line_index = [0]
    y_limt = (xyxy_sort_y['y'][0] + (box_height_mean * 0.9))
    for i,y in enumerate(xyxy_sort_y['y']):
        if y >= y_limt:
            line_index.append(i)
            y_limt = y + (box_height_mean * 0.9)
    line_index.append(len(xyxy_sort_y) - 1)
    #불필요 성분 제거
    xyxy_sort_y = xyxy_sort_y.drop(columns=['index','confidence', 'class','name'])

    #각 행에 대해 x정렬
    i_rev = 0
    line_lst = []
    for i in line_index:
        df = pd.DataFrame({'xmin':[],'ymin':[], 'xmax':[],'ymax':[],'x':[], 'y':[]})
        if i != 0: 
            df = xyxy_sort_y.loc[i_rev:i-1]
            df = df.sort_values(by=['x'])
            df = df.reset_index()
            df = df.drop(columns=['index'])
            line_lst.append(df)
        i_rev = i

    for data in line_lst:
        # y축 평균
        y_mean = data['y'].mean()
        
        dists = []
        add = []
        #붙어있는 바운딩박스 거리
        for i,num in enumerate(data['x']):
            if i != 0:
                if(num - num_rev < box_width_mean * 1.5):
                    dist = num - num_rev
                    dists.append(dist)
                else:
                    add.append(i)
            num_rev = num
        x_dist_mean = sum(dists)/float(len(dists))
        
        print('data',data)
        #바운딩박스 간 빈공간 추가
        add_index = 0
        print(add)
        for i in add:
           print('i',i)
           add_box_num = int((data['x'][i+add_index] - data['x'][i-1+add_index]) / (x_dist_mean))-1
           print('add_box_num',add_box_num)
           for j in range(1,add_box_num+1):
               print('j',j)
               x =  data['x'][i-1+add_index] + x_dist_mean*j
               y = y_mean
               xmin = x - box_width_mean/2
               ymin = y - box_height_mean/2
               xmax = x + box_width_mean/2
               ymax = y + box_height_mean/2
               new_row = pd.DataFrame({'xmin':[xmin],'ymin':[ymin], 'xmax':[xmax],'ymax':[ymax],'x':[x], 'y':[y]})
               print(new_row)
               data = pd.concat([data.iloc[:i-1+add_index],new_row, data.iloc[i-1+add_index:]], ignore_index=True)
               add_index += 1

        #양 끝단 추가
        # x = data['x'][0] - x_dist_mean
        # y = y_mean
        # xmin = x - box_width_mean/2
        # ymin = y - box_height_mean/2
        # xmax = x + box_width_mean/2
        # ymax = y + box_height_mean/2
        # new_row = pd.DataFrame({'xmin':[xmin],'ymin':[ymin], 'xmax':[xmax],'ymax':[ymax],'x':[x], 'y':[y]})
        # data = pd.concat([new_row, data], ignore_index=True)
        # x = data['x'][len(data)-1] + x_dist_mean
        # y = y_mean
        # xmin = x - box_width_mean/2
        # ymin = y - box_height_mean/2
        # xmax = x + box_width_mean/2
        # ymax = y + box_height_mean/2
        # new_row = pd.DataFrame({'xmin':[xmin],'ymin':[ymin], 'xmax':[xmax],'ymax':[ymax],'x':[x], 'y':[y]})
        # data = pd.concat([new_row, data], ignore_index=True)
        
        df = pd.DataFrame({'xmin':[],'ymin':[], 'xmax':[],'ymax':[],'x':[], 'y':[]})
        #바운딩 박스 크기 재정의
        for i in range(len(data)):
            x = data['x'][i]
            y = data['y'][i]
            xmin = x - box_width_mean/2
            ymin = y - box_height_mean/2
            xmax = x + box_width_mean/2
            ymax = y + box_height_mean/2
            new_row = pd.DataFrame({'xmin':[xmin],'ymin':[ymin], 'xmax':[xmax],'ymax':[ymax],'x':[x], 'y':[y]})
            df = df._append(new_row, ignore_index=True)

        sort_data = df.sort_values('x')
        sort_data = sort_data.reset_index()
        sort_data = sort_data.drop(columns=['index'])

        #점자 검사
        bralie_lst = check_all_bralies(img,sort_data)
        print(bralie_lst)
    return bralie_lst

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


def trans_mp3(text, save_mp3, language="ko", ss=False):         
    

    sp = gTTS(                                                  
        text=text,
        lang=language,
        slow=ss
    )
    for file in os.listdir(save_mp3[:7]):
        if file == save_mp3[8:]:
            save_mp3 = save_mp3[:-5] + str(int(save_mp3[-5])+1) + save_mp3[-4:]
    
    sp.save(save_mp3)
        

    if path.exists(save_mp3):                                   
        playsound.playsound(save_mp3)



def main(img):
    img_p = img_post_processing(img)

    #추론
    xyxy = yolo_detect(img_p)
    data_lst = sort_data(xyxy, img_p)

    #점자해석
    result = trans_data(data_lst)
    print(result)
    #사운드출력
    f_name = 'sound'; f_extension = 'mp3'
    i=0
    for file in os.listdir('./data/sound/'):
        if file == f_name + str(i) + '.' + f_extension:
            i+=0
        else:
            break

    trans_mp3(result,save_mp3 = f_name + str(i) + '.' + f_extension)

    # 모든 윈도우 닫기
    cap.release()
    cv.destroyAllWindows()


def calculate_brightness(frame):
    """이미지의 평균 밝기를 계산합니다."""
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    brightness = np.mean(hsv[:, :, 2])  # V 채널의 평균값
    return brightness


if __name__ == '__main__':
    # 비디오 캡처 객체 생성 (기본 카메라를 사용)
    cap = cv.VideoCapture(0)

    if not cap.isOpened():
        print("카메라를 열 수 없습니다.")
        exit()

    # 노출도 초기 설정값
    initial_exposure = cap.get(cv.CAP_PROP_EXPOSURE)
    exposure_value = initial_exposure

    # 목표 밝기 값 (조정 필요)
    target_brightness = 130.0
    adjustment_factor = 0.01  # 노출도 조정 비율

    i = 0
    while True:
        # 프레임 읽기
        ret, frame = cap.read()

        if not ret:
            print("프레임을 읽을 수 없습니다.")
            break

        # 프레임의 현재 밝기를 계산
        current_brightness = calculate_brightness(frame)

        # 밝기를 기반으로 노출도를 조절
        if current_brightness < target_brightness - 10:
            exposure_value += adjustment_factor
            state = 0
        elif current_brightness > target_brightness + 10:
            exposure_value -= adjustment_factor
            state = 0

        # 노출도를 설정
        cap.set(cv.CAP_PROP_EXPOSURE, exposure_value)

        # 현재 노출도 및 밝기를 출력
        actual_exposure = cap.get(cv.CAP_PROP_EXPOSURE)
        if i == 50:
            print(f"현재 노출도: {actual_exposure}, 현재 밝기: {current_brightness}")
        i+=1
        # 프레임을 윈도우에 표시
        cv.imshow('Camera', frame)

        # 'q' 키를 누르면 루프 종료
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
        elif current_brightness > 100:
            if cv.waitKey(1) & 0xFF == ord('r'):
                img = frame
                save_file(img,'img','jpg','./data/input_img')

    # 모든 윈도우 닫기
    cap.release()
    cv.destroyAllWindows()