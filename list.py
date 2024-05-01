#초성 중성 종성이 왔을때 3개의 합 또는 초성 중성이 왔을때 2개의 합의 리스트로 변환이 필요함 . 
#그리고 약자와 종성 / 초성과 약자가 왔을때의 리스트 묶기가 필요함 . 
# 지금 문제점 -> 약어에 붙는 1이 초성과 겹쳐서 숫자는 커버가 가능한데 약어가 커버가 안됨 
INITIAL_LIST = [8, 9, 10, 16, 17, 24, 32, 40, 48, 11, 19, 25, 26]
NEUTRALITY_LIST = [35, 28, 14, 49, 37, 44, 13, 41, 42, 21, 23, 29, 12, 39, 61, 15, 58]
FINAL_LIST = [1, 18, 20, 2, 34, 3, 4, 54, 5, 6, 22, 38, 50, 52, 12]

# 약어
AND_LIST = [14, 9, 18, 34, 29, 37, 49]

# 숫자 : 60 -> 그나마의 희망은XX 숫자들이 초성과만 겹치지 않는구나.... 종성도 겹침.. 
NUM_LIST = [1, 3, 9, 25, 17, 11, 27, 19, 10, 26]

# 약자
SHORT_LIST = [43, 9, 10, 17, 24, 7, 40, 11, 19, 25, 26, 57, 62, 30, 33, 51, 59, 45, 55, 63, 27, 47, 53, 46, 31]

# 띄어쓰기
PASS_LIST = [0]


def split_by_number(lst):
    data_lst = []
    temp = []
    for num in lst:
        if num in PASS_LIST:
            if temp:
                data_lst.append(temp)
                temp = []
            data_lst.append([0])
        elif num in INITIAL_LIST:
            temp.append(num)
            if len(temp) > 1 and temp[-2] in INITIAL_LIST and temp[-1] in NEUTRALITY_LIST:
                data_lst.append(temp[-2:])
                temp = []
        elif num in FINAL_LIST:
            temp.append(num)
            data_lst.append(temp)
            temp = []
        else:
            temp.append(num)
    if temp:
        data_lst.append(temp)

      # 수정된 부분: 1 뒤에 AND_LIST에 있는 숫자가 오는 경우 처리
    for sublist in data_lst:
        for i in range(len(sublist) - 1):
            if sublist[i] == 1 and sublist[i + 1] in AND_LIST:
                sublist[i] = int(str(sublist[i]) + str(sublist[i + 1]))
                sublist.pop(i + 1)
            # 60 뒤에 NUM_LIST에 있는 숫자가 오는 경우 해당 숫자에 200을 더해줌
            elif sublist[i] == 60 and sublist[i + 1] in NUM_LIST:
                sublist[i + 1] += 200
                sublist.pop(i)

    # 수정된 부분: 0도 표시되도록 수정
    result_lst = []
    for sublist in data_lst:
        result_lst.append(sublist)
    return result_lst

# 예시 입력 0을 기준으로 리스트가 분리된다.
input_data_str = input("숫자 리스트를 입력하세요 (쉼표로 구분): ")
input_data = [int(x) for x in input_data_str.split(',')]

# 분할 실행
output_data = split_by_number(input_data)

# 출력
print(output_data)
