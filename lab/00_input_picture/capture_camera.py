import cv2 as cv

def capture():
    save_imgfile = "./img/camera_img.PNG"

    if cv.waitkey() == ord('w'):                    #w키 누를때까지 대기
        cap = cv.VideoCapture(0)                    #메인 카메라를 불러와서 return함
        if not cap.isOpend():                       #메인 카메라 연결실패시 종료    
            print("camera open filed")
            exit()
        else:
            ret, img = cap.read()                   #ret : 이미지 읽기 성공/실패 img : 이미지 데이터
            if not ret:                             #이미지 읽기 실패 시 break
                print("can't read the camera")
            
            cv.imshow('Camera_image', img)          #윈도우창에 이미지 띄우기
            cv.imwrite(save_imgfile, img)           #이미지를 저장
            
            cap.release()                           #객체 할당된 메모리를 풀기
            cv.destroyAllWindows()
            return img

if __name__ == '__main__':
    img = capture()
    cv.imshow('Camera_image', img)
    cv.waitKey()
    cv.destroyAllWindows()