INITIAL_LIST = [8,9,10,16,17,24,32,40,48,11,19,25,26]
NEUTRALITY_LIST = [35,28,14,49,37,44,13,41,42,21,23,51,29,12,39,62,31,15,38,13,28]
FINAL_LIST = [1,18,20,2,34,3,4,57,5,6,22,38,50,52]
#약어
AND_LIST = [15,10,19,35,29,38,50]
#약자
SHORT_LIST = [43,9,10,17,24,7,40,11,19,25,26,57,62,30,33,51,59,45,55,63,27,47,53,46,70,12,57]
#띄어쓰기
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
        else:
            temp.append(num)
    if temp:
        data_lst.append(temp)
    return data_lst

# 예시 입력 0을 기준으로 리스트가 분리된다. 
input_data = [9,35,18,0,9,35,28]

# 분할 실행
output_data = split_by_number(input_data)
print(output_data)
