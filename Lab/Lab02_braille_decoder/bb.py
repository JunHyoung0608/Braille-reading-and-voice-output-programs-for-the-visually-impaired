#초성: 0, 중성: 0, 종성: 0, 약자: 0, 약어 : x, 숫자: 0, 문장부호: x

INITIAL_LIST = {8: 'ㄱ', 9: 'ㄴ', 10: 'ㄷ', 16: 'ㄹ', 17: 'ㅁ', 24: 'ㅂ', 32: 'ㅅ', 40: 'ㅈ', 48: 'ㅊ', 11: 'ㅋ', 19: 'ㅌ', 25: 'ㅍ', 26: 'ㅎ'}
NEUTRALITY_LIST = {35: 'ㅏ', 28: 'ㅑ', 14: 'ㅓ', 49: 'ㅕ', 37: 'ㅗ', 44: 'ㅛ', 13: 'ㅜ', 41: 'ㅠ', 42: 'ㅡ', 21: 'ㅣ', 23: 'ㅐ', 29: 'ㅔ', 12: 'ㅖ', 39: 'ㅘ', 61: 'ㅚ', 15: 'ㅝ', 58: 'ㅢ'}
FINAL_LIST = {1: 'ㄱ', 18: 'ㄴ', 20: 'ㄷ', 2: 'ㄹ', 34: 'ㅁ', 3: 'ㅂ', 4: 'ㅅ', 54: 'ㅇ', 5: 'ㅈ', 6: 'ㅊ', 22: 'ㅋ', 38: 'ㅌ', 50: 'ㅍ', 52: 'ㅎ', 12: 'ㅆ'}
AND_LIST = {14: '그래서', 9: '그러나', 18: '그러면', 34: '그러므로', 29: '그런데', 37: '그리고', 49: '그리하여'}
NUM_LIST = {1: '1', 3: '2', 9: '3', 25: '4', 17: '5', 11: '6', 27: '7', 19: '8', 10: '9', 26: '0'}
SHORT_LIST_BE = {43: '가', 9: '나', 10: '다', 17: '마', 24: '바', 7: '사', 40: '자', 11: '카', 19: '타', 25: '파', 26: '하'}
SHORT_LIST_AF = {57: '억', 62: '언', 30: '얼', 33: '연', 51: '열', 59: '영', 45: '옥', 55: '온', 63: '옹', 27: '운', 47: '울', 53: '은', 46: '을', 31: '인'}
#BUHO_LIST = {25:'.',38:'?',22:'!',16:',',36:'-',38:'"',52:'"'}
# 36,36 => '~', 20,20 => '*', 32,38:''',52,4:''',16,2:':',48,6:';',32,32,32: ...
JUMP = {0:'J'}
NUM = [60]
STRONG = [32]

#input_data = [0,1,14,0,9, 9, 42, 18, 100, 26, 23, 54, 0, 24, 45, 26, 3, 9, 21, 10, 60, 17,8,35,35,28,49]
input_data = [0,1,14,0,35,18,9,49,54,26,32,29,44,40,14,9,53,8,21,34,12,24,21,18,21,3,9,21,10,60,1, 1, 1,0]
result = []
prev_type = None
next_code = None
'''
종류:초성(쌍초성) 중성 종성(종겹받침) 약자 약어 숫자
1. 숫자
2. 약어
3. 약자A -> 약자B
4. 된소리 -> 초성
5. 중성
6. 종성(종겹받침)
'''

def check_kind(index,data):
    result = []
    print(data[index],end=' \t')
                                                                                                                                                                        #숫자
    if data[index] == 60:
        while data[index+1] != 0:
            index += 1; key = data[index]
            print(key)
            result.append(NUM_LIST[key])
                                                                                                                                                                        #약어
    elif (data[index] == 1) and (data[index-1] == 0) and (data[index+1] in AND_LIST) and (data[index+2] == 0):
        index += 1; key = data[index]
        result.append(AND_LIST[key])
                                                                                                                                                                        #약자
    elif data[index] in SHORT_LIST_AF:                                                                                                                                  #약자-AF
        key = data[index]
        result.append(SHORT_LIST_AF[key])
    elif (data[index] in SHORT_LIST_BE) and ((data[index+1] in INITIAL_LIST) or (data[index+1] in SHORT_LIST_BE) or (data[index+1] == 0) or (data[index+1] == NUM)):    #약자-BE
        key = data[index]
        result.append(SHORT_LIST_BE[key])
                                                                                                                                                                        #초성
    elif (data[index] == STRONG) and (data[index+1] in INITIAL_LIST):                                                                                                   #초성-된소리
        index += 1; key = data[index]
        result.append(SHORT_LIST_BE[key])

    elif data[index] in INITIAL_LIST:                                                                                                                                   #초성
        key = data[index]
        result.append(INITIAL_LIST[key])
                                                                                                                                                                        #중성
                                                                                                                                                                        #두글자 중성 추가
    elif data[index] in NEUTRALITY_LIST:                                                                                                             
        key = data[index]
        if (data[index-1] not in INITIAL_LIST) or (data[index-1] == 0):
            result.append('ㅇ')
        result.append(NEUTRALITY_LIST[key])
                                                                                                                                                                        #종성
    elif (data[index] in FINAL_LIST) and (data[index+1] in FINAL_LIST):                                                                                                 #종성-곁받침
        #곁받침
        a=1
    elif (data[index] in FINAL_LIST):                                                                                                                                   #종성
        key = data[index]
        result.append(FINAL_LIST[key])

    elif data[index] in JUMP:                                                                                                                                           #띄어쓰기
        result.append('p')

    return index+1,result


def trans_data2(input_data):
    index = 0
    txt = []
    while len(input_data) > index:
        index, result = check_kind(index,input_data)
        txt += result
        
        print(index+1,'\t',result)
    return txt


    
if __name__ == "__main__":
    input_data = [35,18,9,49,54,26,32,29,44,40,14,9,53,8,21,34,12,24,21,18,21,3,9,21,10,0,60,1,0]
    input_data2 = [0,1,14,0,35,18,9,49,54,26,32,29,44,40,14,9,53,8,21,34,12,24,21,18,21,3,9,21,10,0,60,1, 1, 1,0]

    print('input\t','index\t','value')
    txt = trans_data2(input_data2)
    print('----------------------------------------')
    print('result:',txt)