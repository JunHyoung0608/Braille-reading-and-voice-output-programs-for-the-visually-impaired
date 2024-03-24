# 201921310 이준형 201921319 채민석 PYTHON 사용
# 0~2번까지는 수행했으나, 3번. 로고 색변환 안되었습니다.
from PIL import Image
import numpy as np
from skimage import feature, transform, filters, measure, draw
from skimage.transform import hough_line, hough_line_peaks
from skimage.feature import match_template
import matplotlib.pyplot as plt
from shapely.geometry import Polygon

# 이미지 파일 로드
img = Image.open('su1.jpg')

# 이미지를 그레이스케일로 변환
img = img.convert('L')

# 이미지를 numpy 배열로 변환
np_img = np.array(img)

# 이미지 패딩 (흰색으로)
pad_width = max(np_img.shape)
padded_img = np.pad(np_img, pad_width, mode='constant', constant_values=255)

# 캐니 엣지 검출
edges = feature.canny(padded_img, sigma=8)

# 허프 변환을 이용한 직선 검출
hspace, angles, dists = hough_line(edges)

# 피크값 찾기 (임계값 조절)
for _, angle, dist in zip(*hough_line_peaks(hspace, angles, dists, threshold=0.8 * hspace.max())): # threshold 값을 조절
    y0 = (dist - 0 * np.cos(angle)) / np.sin(angle)
    y1 = (dist - padded_img.shape[1] * np.cos(angle)) / np.sin(angle)

# 선의 기울기를 계산
slope = (y1 - y0) / (padded_img.shape[1] - 0)

# 기울기를 기반으로 회전 각도를 계산 (90도를 더하거나 빼서 수평이 되도록 조정)
rotation_angle = np.arctan(slope) * 180 / np.pi

# 이미지를 회전
rotated_img = transform.rotate(padded_img, rotation_angle, cval=1)

# 두 번째 이미지 로드
img2 = Image.open('su2.jpg')
img2 = img2.convert('L')
np_img2 = np.array(img2)

# match_template 함수를 이용하여 로테이트 된 이미지(rotated_img)와 두 번째 이미지(np_img2) 비교
result = match_template(rotated_img, np_img2)

# 매칭 결과에서 가장 높은 값의 위치 찾기
ij = np.unravel_index(np.argmax(result), result.shape)
x, y = ij[::-1]

# 세 번째 이미지 로드
img3 = Image.open('su3.jpg')
img3 = img3.convert('L')
np_img3 = np.array(img3)

# 히스토그램 계산
hist_rotated_img, _ = np.histogram(rotated_img.flatten(), bins=256, range=[0,256])
hist_img3, _ = np.histogram(np_img3.flatten(), bins=256, range=[0,256])

# 히스토그램 정규화
hist_rotated_img = hist_rotated_img / hist_rotated_img.sum()
hist_img3 = hist_img3 / hist_img3.sum()

# 히스토그램 비교
similarity = np.sum((hist_rotated_img - hist_img3) ** 2 / (hist_rotated_img + hist_img3 + 1e-10))

# 유사도를 100분위로 표시
similarity_percentage = (1 - similarity) * 100

print(f'The similarity between the rotated image and img3 is: {similarity_percentage}%')

# 이미지 그레이스케일 변환 없이 이미지를 사용
gray = np_img3
# dfdfadfa
# 이진화
binary = gray > filters.threshold_otsu(gray)

# 윤곽선 찾기
contours = measure.find_contours(binary, level=0.8)

# 전체 이미지의 평균 픽셀 값 계산
mean_img = np.mean(gray)

max_diff = 0
max_diff_rect = None

for contour in contours:
    # 사각형 찾기
    polygon = Polygon(contour)
    if len(polygon.exterior.coords) == 5:
        # 사각형 내부의 평균 픽셀 값 계산
        mask = np.zeros_like(gray, dtype=bool)
        rr, cc = draw.polygon(contour[:,0], contour[:,1], mask.shape)
        mask[rr, cc] = True
        mean_rect = np.mean(gray[mask])

        # 차이 계산
        diff = abs(mean_img - mean_rect)

        # 차이가 이전의 최대 차이보다 크다면, 이 사각형을 저장
        if diff > max_diff:
            max_diff = diff
            max_diff_rect = contour

# 가장 차이가 큰 사각형의 픽셀 값 변경
if max_diff_rect is not None:
    mask = np.zeros_like(gray, dtype=bool)
    rr, cc = draw.polygon(max_diff_rect[:,0], max_diff_rect[:,1], mask.shape)
    mask[rr, cc] = True
    np_img3[mask] = 255
    np_img3[(gray > 0.5) & mask] = 255
    np_img3_color = np.stack([np_img3]*3, axis=-1)
    np_img3_color[mask] = [0, 0, 255]  # 변경된 부분을 파란색으로 표시

# 결과 그리기 - 로테이트 된 이미지, 매칭된 템플릿, 변경된 부분 표시
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
axes[0].imshow(rotated_img, cmap=plt.cm.gray, aspect='auto')
axes[0].axis('off')
axes[1].imshow(rotated_img, cmap=plt.cm.gray, aspect='auto')
h, w = np_img2.shape
rect = plt.Rectangle((x, y), w, h, edgecolor='r', facecolor='none')
axes[1].add_patch(rect)
axes[1].axis('off')
axes[2].imshow(np_img3_color)
axes[2].axis('off')

plt.show()
