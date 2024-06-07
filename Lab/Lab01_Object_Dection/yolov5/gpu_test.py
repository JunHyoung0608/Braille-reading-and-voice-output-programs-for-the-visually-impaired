import tensorflow as tf
import torch




# CUDA가 사용 가능한지 확인
if torch.cuda.is_available():
    # 현재 사용 가능한 CUDA 장치 수를 출력
    print("CUDA 장치가 사용 가능합니다.")
    print("사용 가능한 CUDA 장치 수:", torch.cuda.device_count())

    # 현재 선택된 CUDA 장치의 이름 출력
    print("현재 CUDA 장치:", torch.cuda.get_device_name(torch.cuda.current_device()))

    # CUDA로 텐서를 생성하고 연산 수행
    device = torch.device("cuda")          # CUDA 장치를 사용하기 위한 장치 객체 생성
    x = torch.tensor([1.0, 2.0]).to(device)  # CUDA 장치로 텐서 이동
    y = torch.tensor([3.0, 4.0]).to(device)  # CUDA 장치로 텐서 이동
    z = x + y                              # CUDA 장치에서 텐서 연산 수행
    print("CUDA를 통해 연산된 결과:", z)

else:
    print("CUDA 장치를 사용할 수 없습니다. CPU를 사용합니다.")

print(torch.cuda.is_available())