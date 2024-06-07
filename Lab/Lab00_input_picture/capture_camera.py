import cv2 as cv
save_imgfile = "./img/camera_img.PNG"

def capture(save_imgfile, width, height):
    
    cap = cv.VideoCapture(0)                        #메인 카메라를 불러와서 return함
    cap.set(cv.CAP_PROP_FRAME_WIDTH, width)         #카메라 너비 = 640
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, height)       #카메라 높이 = 480
    #cap.set(cv.CAP_PROP_AUTO_EXPOSURE, 0)           # 자동 노출 비활성화
    #cap.set(cv.CAP_PROP_EXPOSURE, 1.0)              # 노출 조절 (0.0 ~ 1.0)
    #cap.set(cv.CAP_PROP_BRIGHTNESS, 1.0)


    if not cap.isOpened():                          #메인 카메라 연결실패시 종료    
        print("Error : Camera connection filed")
        exit()
    else:
        ret, img = cap.read()                       #ret : 이미지 읽기 성공/실패 img : 이미지 데이터
        if not ret:                                 #이미지 읽기 실패 시 break
            print("Error : Can't read the camera data")
            return None
            
    cv.imwrite(save_imgfile, img)                   #이미지를 저장
                
    cap.release()                                   #객체 할당된 메모리를 풀기
    return img

if __name__ == '__main__':
    img = capture(save_imgfile, 640, 480)
    if img is not None:
        cv.imshow('Camera_image', img)
        cv.waitKey(0)
        cv.destroyAllWindows()
    else :
        print("error : Don't have image file" )