#추론한 데이터의 좌표와 문자를 받아와 합성과 문장 검사를 목표로 한다
#https://github.com/ultralytics/yolov5/issues/36
import os 
import torch
import pandas as pd

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


if __name__ == '__main__':
    input_img = './data/images/bbang_02_jpg.rf.ae3fe8719a3d3cb2527af38bc52e8b8a.jpg'
    xyxy = yolo_detect(input_img)

    data_lst = sort_data(xyxy)
    print(data_lst)





