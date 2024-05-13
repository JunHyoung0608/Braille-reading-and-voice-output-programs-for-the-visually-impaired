#초성: o, 중성: o, 종성: o, 약자: o, 약어 : o, 숫자: o, 문장부호: x
#https://en.wikipedia.org/wiki/Hangul_Jamo_(Unicode_block)
INITIAL_LIST = {8: 0x1100, 9: 0x1102, 10: 0x1103, 16: 0x1105, 17: 0x1106, 24: 0x1107, 32: 0x1109, 40: 0x110C, 48: 0x110E, 11: 0x110F, 19: 0x1110, 25: 0x1111, 26: 0x1112}
NEUTRALITY_LIST = {35: 0x1161, 28: 0x1163, 14: 0x1165, 49: 0x1167, 37: 0x1169, 44: 0x116D, 13: 0x116E, 41: 0x1172, 42: 0x1173, 21: 0x1175, 23: 0x1162, 29: 0x1166, 12: 0x1168, 39: 0x116A, 61: 0x116C, 15: 0x116F, 58: 0x1164}
FINAL_LIST = {1: 0x11A8, 18: 0x11AB, 20: 0x11AE, 2: 0x11AF, 34: 0x11B7, 3: 0x11B8, 4: 0x11BA, 54: 0x11BC, 5: 0x11BD, 6: 0x11BE, 22: 0x11BF, 38: 0x11B0, 50: 0x11B1, 52: 0x11B2}
AND_LIST = {14:[0x1100,0x1173,0x1105,0x1162,0x1109,0x1165], 
            9:[0x1100,0x1173,0x1105,0x1165,0x1102,0x1161], 
            18:[0x1100,0x1173,0x1105,0x1165,0x1106,0x1167,0x11AB], 
            34:[0x1100,0x1173,0x1105,0x1165,0x1106,0x1173,0x1105,0x1169], 
            29:[0x1100,0x1173,0x1105,0x1165,0x11AB,0x1103,0x1166], 
            37:[0x1100,0x1173,0x1105,0x1175,0x1100,0x1169], 
            49:[0x1100,0x1173,0x1105,0x1175,0x1112,0x1161,0x110B,0x1167]}
NUM_LIST = {1: '1', 3: '2', 9: '3', 25: '4', 17: '5', 11: '6', 27: '7', 19: '8', 10: '9', 26: '0'}
SHORT_LIST_BE = {43: 0x1100, 9: 0x1102, 10: 0x1103, 17: 0x1105, 24: 0x1106, 7: 0x1107, 40: 0x110C, 11: 0x110F, 19: 0x1110, 25: 0x1111, 26: 0x1112}
SHORT_LIST_AF = {57: [0x1165,0x11A8], 62:[0x1165,0x11AB], 30:[0x1165,0x11AF], 33:[0x1167,0x11AB], 51:[0x1167,0x11AF], 59:[0x1167,0x11BC], 45:[0x1169,0x11A8], 55:[0x1169,0x11AB], 63:[0x1169,0x11BC], 27:[0x116E,0x11AB], 47:[0x116E,0x11AF], 53:[0x1173,0x11AB], 46:[0x1173,0x11AF], 31:[0x1175,0x11AB]}
#BUHO_LIST = {25:'.',38:'?',22:'!',16:',',36:'-',38:'"',52:'"'}
# 36,36 => '~', 20,20 => '*', 32,38:''',52,4:''',16,2:':',48,6:';',32,32,32: ...
NUM = 60; STRONG = 32

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
    if data[index] == NUM:                                                                        
        while data[index+1] != 0:
            index += 1; key = data[index]
            result.append(NUM_LIST[key])
    #약어                                                                                                                                                               
    elif (data[index] == 1) and (data[index-1] == 0) and (data[index+1] in AND_LIST) and (data[index+2] == 0):
        key = data[index+1]
        result += AND_LIST[key]
        index += 1
    #약자-AF                                                                                                                                                                  
    elif data[index] in SHORT_LIST_AF:  
        key = data[index]
        if (data[index-1] not in INITIAL_LIST) or (data[index-1] == 0):
            kind += '+'
            result.append(0x110B)
        result += SHORT_LIST_AF[key]
    #약자-BE
    elif (data[index] in SHORT_LIST_BE) and ((data[index+1] in INITIAL_LIST) or (data[index+1] in SHORT_LIST_AF) or (data[index+1] in SHORT_LIST_BE) or (data[index+1] == 0) or (data[index+1] == NUM) or (data[index+1] in FINAL_LIST)):
        key = data[index]
        result.append(SHORT_LIST_BE[key]); result.append(0x1161)   #reuslt <=== [value,0x1161(ㅏ)]
    #초성-된소리                                                                                                                                                       
    elif (data[index] == STRONG) and (data[index+1] in INITIAL_LIST):                                                                                                                                                              
        key = data[index+1]
        result.append(INITIAL_LIST[key])
        index += 1
    #초성
    elif data[index] in INITIAL_LIST:
        key = data[index]
        result.append(INITIAL_LIST[key])
    #중성 
    elif data[index] in NEUTRALITY_LIST:                                                                                                                                                                                                                                          
        key = data[index]
        if (data[index-1] not in INITIAL_LIST) or (data[index-1] == 0):
            result.append(0x110B)
        if (data[index+1] == 23):
            if  (data[index] == 39):    #ㅙ
                result.append(0x116B)
            elif data[index] == 15:     #ㅞ
                result.append(0x1170)
            elif data[index] == 13:     #ㅟ
                result.append(0x1171)
            index += 1
        else:
            result.append(NEUTRALITY_LIST[key])
    #종성-곁받침
    elif (data[index] in FINAL_LIST) and (data[index+1] in FINAL_LIST):
        if data[index] == 1:
            if data[index+1] == 1:      #ㄲ
                result.append(0x11A9)
            elif data[index+1] == 4:    #ㄳ
                result.append(0x11AA)
        elif data[index] == 18:
            if data[index+1] == 5:      #ㄵ
                result.append(0x11AC)
            elif data[index+1] == 52:   #ㄶ
                result.append(0x11AD)
        elif data[index] == 2:
            if data[index+1] == 1:      #ㄺ
                result.append(0x11B0)
            elif data[index+1] == 34:   #ㄻ
                result.append(0x11B1)
            elif data[index+1] == 3:    #ㄼ
                result.append(0x11B2)
            elif data[index+1] == 4:    #ㄽ
                result.append(0x11B3)
            elif data[index+1] == 38:   #ㄾ
                result.append(0x11B4)
            elif data[index+1] == 50:   #ㄿ
                result.append(0x11B5)
            elif data[index+1] == 52:   #ㅀ
                result.append(0x11B6)
        elif data[index] == 3:
            if data[index+1] == 4:      #ㅄ
                result.append(0x11B9)
        elif data[index] == 4:
            if data[index+1] == 4:      #ㅆ
                result.append(0x11BB)
        index += 1
    #종성
    elif data[index] in FINAL_LIST:                                                                                                                                   
        key = data[index]
        result.append(FINAL_LIST[key])
    #띄어쓰기
    elif data[index] == 0:                                                                                                                                         
        result.append('p')

    return index+1, result



def trans_data(input_data):
    print('input\t','index\t','value\t\t','kind',)
    index = 0
    txt = []
    uni = []
    uni_lst = []
    result = []
    
    while len(input_data) > index:
        print(input_data[index],end=' ')

        index, uni = check_kind(index,input_data)
        
        
        uni_lst += uni
        print('\t',index+1,'\t',uni)
    return uni_lst

def combine(initial_index, neutrality_index, final_index=None):

    if final_index is None:
        final_index = 0

    # 유니코드 계산
    unicode_value = 0xAC00 + (initial_index * 21 * 28) + (neutrality_index * 28) + final_index
    return chr(unicode_value)

def trans_uni2txt(uni_lst):
    start_p = 0
    end_p = 0
    kind = ''
    txt = ''
    for index,uni in enumerate(uni_lst):
        if(uni >= 0x1100) and (uni <= 0x1112):
            kind = 'INITIAL'
        elif(uni >= 0x1161) and (uni <= 0x1175):
            kind = 'NEUTRALITY'
        elif(uni >= 0x11A8) and (uni <= 0x11C2):
            kind = 'FINAL'
        else:
            kind = 'OTHRT'


        if start_p > end_p:
            if (kind == 'INITIAL') or (kind == 'OTHRT'):
                end_p = index-1
                initial_index = 0x1100 - uni_lst[start_p]
                neutrality_index = 0x1161 - uni_lst[start_p+1]
                if (end_p - start_p) == 1:
                    final_index = None
                elif (end_p - start_p) == 2:
                    final_index = 0x11A8 - uni_lst[start_p+2] + 1
                
                txt+=combine(initial_index,neutrality_index,final_index)
        elif start_p == end_p:
            if (kind == 'INITIAL'):
                start_p = index        


    return txt

    
if __name__ == "__main__":
    input_data1 = [35,18,9,49,54,26,32,29,44,40,14,9,53,8,21,34,12,24,21,18,21,3,9,21,10,0,60,1,0]
    input_data2 = [0,1,14,0,35,18,9,49,54,26,32,29,44,40,14,9,53,8,21,34,12,24,21,18,21,3,9,21,10,0,60,1, 1, 1,0]
    input_data3 = [9,9,42,18,100,26,23,54,0,24,45,26,3,9,21,10,60,17,0]
    input_data4 = [12,4,12,4,29,0,14,9,42,0,26,18,0,17,46,29,0,35,21,10,46,21,0,7,2,8,37,21,4,4,14,4,4,32,42,3,9,21,10,0]
    txt = trans_data(input_data4)
    print('----------------------------------------')
    print('result:',txt)