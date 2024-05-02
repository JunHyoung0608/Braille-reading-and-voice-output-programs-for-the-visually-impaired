#문제점 1. 빈 리스트가 반환됨 
#문제점 2. 이거 왜그런지 모르겠는데 input에 24 다음에 45가 오는데 자꾸 24에 24가 뒤에 옴
#문제점 3. 숫자가 하나의 리스트로 묶여야하는데 하나의 리스트로 안묶이는 중 
INITIAL_LIST = [8, 9, 10, 16, 17, 24, 32, 40, 48, 11, 19, 25, 26]
NEUTRALITY_LIST = [35, 28, 14, 49, 37, 44, 13, 41, 42, 21, 23, 29, 12, 39, 61, 15, 58]
FINAL_LIST = [1, 18, 20, 2, 34, 3, 4, 54, 5, 6, 22, 38, 50, 52, 12]

AND_LIST = [14, 9, 18, 34, 29, 37, 49]
NUM_LIST = [1, 3, 9, 25, 17, 11, 27, 19, 10, 26]

SHORT_LIST = [43, 9, 10, 17, 24, 7, 40, 11, 19, 25, 26, 57, 62, 30, 33, 51, 59, 45, 55, 63, 27, 47, 53, 46, 31]
PASS_LIST = [0]

def split_list(lst):
    result = []
    temp = []
    for num in lst:
        if num in INITIAL_LIST:
            if temp:
                if len(temp) == 2 and temp[-1] in NEUTRALITY_LIST:
                    temp.append(num)
                    result.append(temp)
                    temp = []
                else:
                    result.append(temp)
                    temp = [num]
            else:
                temp.append(num)
        elif num in NEUTRALITY_LIST:
            if temp and temp[-1] in INITIAL_LIST:
                temp.append(num)
            else:
                result.append(temp)
                temp = [num]
        elif num in FINAL_LIST:
            if temp and temp[-1] in NEUTRALITY_LIST:
                temp.append(num)
                result.append(temp)
                temp = []
            else:
                temp.append(num)
        elif num in SHORT_LIST[:10]:
            if temp:
                result.append(temp)
                temp = [num]
            else:
                temp.append(num)
        elif num in SHORT_LIST[10:]:
            if temp and temp[-1] in INITIAL_LIST:
                result.append(temp)
            else:
                temp.append(num)
                temp = [num]
        elif num in AND_LIST:
            if temp and temp[-1] == 1:
                temp[-1] = 10 + num
            else:
                result.append(temp)
                temp = [num]
        elif num == 60:  # 숫자 60인 경우
            if temp and temp[-1] == 60:  # 숫자 60 뒤에 NUM_LIST인 경우
                temp[-1] = 600 + num
            elif temp and temp[-1] in NUM_LIST:  # 숫자 60 뒤에 NUM_LIST의 숫자가 오는 경우
                temp[-1] = 600 + num
            else:
                result.append(temp)
                temp = [num]
        elif num == 0:
            result.append([0])
    if temp:
        result.append(temp)
    return result

# 예시 입력
input_data_str = "9,9,42,18,0,26,23,54,24,45,26,3,9,21,10,60,17"
input_data = [int(x) for x in input_data_str.split(',')]

# 분할 실행
output_data = split_list(input_data)

# 출력
print(output_data)
