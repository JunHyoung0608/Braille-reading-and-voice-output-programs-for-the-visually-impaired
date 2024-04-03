import cv2

def histogram_equalization(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    equalized_image = cv2.equalizeHist(gray_image)
    return cv2.cvtColor(equalized_image, cv2.COLOR_GRAY2BGR)

if __name__ == "__main__":
    # 이미지 불러오기
    image = cv2.imread("./img/camera_img.PNG")

    # 히스토그램 평활화 적용
    equalized_image = histogram_equalization(image)

    # 결과 이미지 출력
    cv2.imshow("Original Image", image)
    cv2.imshow("Equalized Image", equalized_image)
    cv2.imshow("aaa", image +20)
    cv2.waitKey(0)
    cv2.destroyAllWindows()