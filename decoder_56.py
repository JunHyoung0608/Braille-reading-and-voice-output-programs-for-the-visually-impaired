
INITIAL_LIST = {8: 0x1100, 9: 0x1102, 10: 0x1103, 16: 0x1105, 17: 0x1106, 24: 0x1107, 32:0x1109 , 40: 0x110C, 48: 0x110E, 11: 0x110F, 19: 0x1110, 25: 0x1111, 26: 0x1112}
NEUTRALITY_LIST = {35: 0x1161, 28: 0x1163, 14: 0x1165, 49: 0x1167, 37:0x1169, 44: 0x116D, 13: 0x116E, 41: 0x1172, 42: 0x1173, 21: 0x1175, 23: 0x1162, 29: 0x1166 , 12: 0x1168, 39: 0x116A, 61:0x116C, 15: 0x116F, 58: 0x1174}
FINAL_LIST = {1: 0x11A8, 18: 0x11AB, 20: 0x11AE, 2: 0x11AF, 34: 0x11B7, 3: 0x11B8, 4: 0x11BA, 54: 0x11BC, 5: 0x11BD, 6: 0x11BE, 22: 0x11BF, 38: 0x11C0, 50: 0x11C1, 52: 0x11C2}
AND_LIST = {
    14: '\uADF8\uB798\uC11C',
    9: '\uADF8\uB7EC\uB098',
    18: '\uADF8\uB7EC\uBA74',
    34: '\uADF8\uB7EC\uBBC0\uB85C',
    29: '\uADF8\uB7F0\uB370',
    37: '\uADF8\uB9AC\uC560',
    49: '\uADF8\uB9AC\uD558\uC5EC'
}
NUM_LIST = {1: 0x0031, 3: 0x0032, 9: 0x0033, 25: 0x0034, 17: 0x0035, 11: 0x0036, 27: 0x0037, 19: 0x0038, 10: 0x0039, 26: 0x0030}
SHORT_LIST_BE = {43: 0xAC00, 9: 0xB098, 10: 0xB2E4, 17: 0xBC14, 24: 0xBC14, 7: 0xC0AC, 40: 0xC790, 11: 0xCE74, 19: 0xD0C0, 25: 0xD30C, 26: 0xD558}
SHORT_LIST_AF = {57: 0xC5B5, 62: 0xC5B8, 30: 0xC5BC, 33: 0xC5D0, 51: 0xC5F0, 59: 0xC601, 45: 0xC625, 55: 0xC628, 63: 0xC639, 27: 0xC740, 47: 0xC758, 53: 0xC740, 46: 0xC744, 31: 0xC778}
JUMP = {0:'J'}
NUM = [60]
STRONG = [32]

result = []
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
    elif (data[index] in SHORT_LIST_BE) and ((data[index+1] in INITIAL_LIST) or (data[index+1] in SHORT_LIST_AF) or (data[index+1] in SHORT_LIST_BE) or (data[index+1] == 0) or (data[index+1] == 60) or (data[index+1] in FINAL_LIST)):    #약자-BE
        key = data[index]
        result.append(SHORT_LIST_BE[key])
                                                                                                                                                                        #초성
    elif (data[index] == STRONG) and (data[index+1] in INITIAL_LIST):                                                                                                   #초성-된소리
        index += 1; key = data[index]
        result.append(INITIAL_LIST[key])

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
        index += 1
        #곁받침
        a=1
    elif data[index] in FINAL_LIST:                                                                                                                                   #종성
        key = data[index]
        result.append(FINAL_LIST[key])

    elif data[index] in JUMP:                                                                                                                                           #띄어쓰기
        result.append('p')

    return index+1,result


def trans_data5(input_data):
    index = 0
    txt = []
    while len(input_data) > index:
        print(input_data[index],end=' ')
        index, result = check_kind(index,input_data)
        txt += result
        
        print('\t',index+1,'\t',result)
    return txt


    
if __name__ == "__main__":
    input_data1 = [35,18,9,49,54,26,32,29,44,40,14,9,53,8,21,34,12,24,21,18,21,3,9,21,10,0,60,1,0]
    input_data2 = [0,1,14,0,35,18,9,49,54,26,32,29,44,40,14,9,53,8,21,34,12,24,21,18,21,3,9,21,10,0,60,1, 1, 1,0]
    input_data3 = [9,9,42,18,100,26,23,54,0,24,45,26,3,9,21,10,60,17,0]
    input_data4 = [12,4,12,4,29,0,14,9,42,0,26,18,0,17,46,29,0,35,21,10,46,21,0,7,2,8,37,21,32,32,14,32,32,32,42,3,9,21,10,0]
    input_data5 = [35,18,9,49,54,26,32,29,44,0,40,14,26,58,9,42,18,0,32,21,32,42,19,29,34,24,35,18,10,37,48,29,8,37,54,26,35,1,8,39,0,21,3,9,21,10,0]


    print('input\t','index\t','value')
    txt = trans_data5(input_data5)
    print('----------------------------------------')
    print('result:',txt)
