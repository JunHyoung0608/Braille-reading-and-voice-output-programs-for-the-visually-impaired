import cv2
import numpy as np

def calculate_brightness(frame):
    """이미지의 평균 밝기를 계산합니다."""
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    brightness = np.mean(hsv[:, :, 2])  # V 채널의 평균값
    return brightness

# 비디오 캡처 객체 생성 (기본 카메라를 사용)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("카메라를 열 수 없습니다.")
    exit()

# 노출도 초기 설정값
initial_exposure = cap.get(cv2.CAP_PROP_EXPOSURE)
exposure_value = initial_exposure

# 목표 밝기 값 (조정 필요)
target_brightness = 130.0
adjustment_factor = 0.01  # 노출도 조정 비율

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
    cap.set(cv2.CAP_PROP_EXPOSURE, exposure_value)

    # 현재 노출도 및 밝기를 출력
    actual_exposure = cap.get(cv2.CAP_PROP_EXPOSURE)
    print(f"현재 노출도: {actual_exposure}, 현재 밝기: {current_brightness}")
    # 프레임을 윈도우에 표시
    cv2.imshow('Camera', frame)

    # 'q' 키를 누르면 루프 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    elif current_brightness > 100:
        if cv2.waitKey(1) & 0xFF == ord('r'):
            img = frame
            cv2.imshow('img', img)

# 모든 윈도우 닫기
cap.release()
cv2.destroyAllWindows()