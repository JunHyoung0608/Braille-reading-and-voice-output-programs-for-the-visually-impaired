#5/10 12:16am
#고민해볼것 : 모음 2번/ 12: ㅆ 고민 / index 고민(pop말고 del로 해결 완료)

INITIAL_LIST = {8: 'ㄱ', 9: 'ㄴ', 10: 'ㄷ', 16: 'ㄹ', 17: 'ㅁ', 24: 'ㅂ', 32: 'ㅅ', 40: 'ㅈ', 48: 'ㅊ', 11: 'ㅋ', 19: 'ㅌ', 25: 'ㅍ', 26: 'ㅎ'}
NEUTRALITY_LIST = {35: 'ㅏ', 28: 'ㅑ', 14: 'ㅓ', 49: 'ㅕ', 37: 'ㅗ', 44: 'ㅛ', 13: 'ㅜ', 41: 'ㅠ', 42: 'ㅡ', 21: 'ㅣ', 23: 'ㅐ', 29: 'ㅔ', 12: 'ㅖ', 39: 'ㅘ', 61: 'ㅚ', 15: 'ㅝ', 58: 'ㅢ'}
FINAL_LIST = {1: 'ㄱ', 18: 'ㄴ', 20: 'ㄷ', 2: 'ㄹ', 34: 'ㅁ', 3: 'ㅂ', 4: 'ㅅ', 54: 'ㅇ', 5: 'ㅈ', 6: 'ㅊ', 22: 'ㅋ', 38: 'ㅌ', 50: 'ㅍ', 52: 'ㅎ', 12: 'ㅆ'}
AND_LIST = {14: '그래서', 9: '그러나', 18: '그러면', 34: '그러므로', 29: '그런데', 37: '그리고', 49: '그리하여'}
NUM_LIST = {1: '1', 3: '2', 9: '3', 25: '4', 17: '5', 11: '6', 27: '7', 19: '8', 10: '9', 26: '0'}
SHORT_LIST_BE = {43: '가', 9: '나', 10: '다', 17: '마', 24: '바', 7: '사', 40: '자', 11: '카', 19: '타', 25: '파', 26: '하'}
SHORT_LIST_AF = {57: '억', 62: '언', 30: '얼', 33: '연', 51: '열', 59: '영', 45: '옥', 55: '온', 63: '옹', 27: '운', 47: '울', 53: '은', 46: '을', 31: '인'}
JUMP = {0:'J'}
NUM = [60]
SAME = [32]

input_data = [12,4,9,2,12,4,9,2,29,0,14,9,42,0,26,18,0,17,46,29,0,35,21,10,46,21,0,7,2,8,37,0,21,12,14,12,32,42,3,9,21,10,35,60,19,8,35,3,4]

result = []
prev_type = None
next_code = None
prev_code = None

#enumerate : 반복 순회함수 , i = 현재 인덱스, next_code = 다음 인덱스, prev_code = 이전 인덱스
for i, code in enumerate(input_data):
    if i < len(input_data) - 1:
        next_code = input_data[i + 1]
    else:
        next_code = None
    
    if i > 0:
        prev_code = input_data[i - 1]
    else:
        prev_code = None

if code in INITIAL_LIST: # 초성 
    if next_code in [8,10,24,32,40] and next_code in NEUTRALITY_LIST and next_code in SHORT_LIST_AF: #중성과 약어 앞에 오면서 32와 동반하여 저 숫자가 왔을경우 
        input_data.pop(code)
        if next_code == 8:
            result.append('ㄲ')
        elif next_code == 10:
            result.append('ㄸ')
        elif next_code == 24:
            result.append('ㅃ')
        elif next_code == 32:
            result.append('ㅆ')
        elif next_code == 40:
            result.append('ㅉ')
    elif next_code in NEUTRALITY_LIST and next_code in SHORT_LIST_AF: # 중성과 약어 앞에 올 경우
        result.append(INITIAL_LIST[code])

elif code in NEUTRALITY_LIST: #중성 
    if prev_type == 'INI': # 초성이 있을때
       result.append(NEUTRALITY_LIST[code])
       #prev_type = 'NEU'
    elif prev_type != 'INI': # 초성이 오지 않았을때 단독 쓰임 
        result.append('ㅇ')
        result.append(NEUTRALITY_LIST[code])
        #prev_type = 'NEU'
# 두글자 모음 추가하기 


elif code in FINAL_LIST: # 종성 
    if prev_code in NEUTRALITY_LIST or prev_code in SHORT_LIST_BE and next_code not in FINAL_LIST: #앞에 중성 또는 약어가 있을때, 뒤에 종성 숫자가 반복되지 않을때 
        result.append(FINAL_LIST[code])                                                             #밑에 겹받침을 위한 제한
    if code in [1,2,3,4] and next_code in [1,3,4,5,34,38,50,52]: #현재코드가 1,2,3,4중에 있으면서 다음 숫자가 저 안에 있다면
        if code == 1 and next_code == 4:
           del input_data[i] # 하나의 값만을 반환해야하기때문에 현재 코드와 다음 코드를 지우고
           del input_data[i+1] # 결과값에 ㄳ 이라는 값을 하나 넣는다.
           result.append('ㄳ')
        elif code == 4 and next_code == 5:
           del input_data[i]
           del input_data[i+1] 
           result.append('ㄵ')
        elif code == 4 and next_code == 52:
           del input_data[i]
           del input_data[i+1] 
           result.append('ㄶ')
        elif code == 2 and next_code == 1:
           del input_data[i]
           del input_data[i+1] 
           result.append('ㄺ')
        elif code == 2 and next_code == 34:
           del input_data[i]
           del input_data[i+1] 
           result.append('ㄻ')
        elif code == 2 and next_code == 3:
           del input_data[i]
           del input_data[i+1] 
           result.append('ㄼ')
        elif code == 2 and next_code == 4:
           del input_data[i]
           del input_data[i+1] 
           result.append('ㄽ')
        elif code == 2 and next_code == 38:
           del input_data[i]
           del input_data[i+1] 
           result.append('ㄾ')
        elif code == 2 and next_code == 50:
           del input_data[i]
           del input_data[i+1] 
           result.append('ㄿ')
        elif code == 2 and next_code == 52:
           del input_data[i]
           del input_data[i+1] 
           result.append('ㅀ')
        elif code == 3 and next_code == 4:
           del input_data[i]
           del input_data[i+1] 
           result.append('ㅄ')
        elif code == 1 and next_code == 1:
            del input_data[i]
            del input_data[i+1] 
            result.append('ㄲ')

elif code in SHORT_LIST_BE: #약어 가,나,다 등 
    if next_code in FINAL_LIST: #뒤에 종성이 올 경우
        result.append(SHORT_LIST_AF[code])
    if next_code not in FINAL_LIST: # 뒤에 종성이 오지 않는다면 
        result.append(SHORT_LIST_AF[code])

elif code in SHORT_LIST_AF: #약어 억,언,얼 등 
    if prev_code in INITIAL_LIST and next_code not in FINAL_LIST: #앞에 초성은 올 수 있지만 뒤에 종성은 올수 없음
        result.append(SHORT_LIST_AF[code])
    elif prev_code not in INITIAL_LIST and prev_code not in NEUTRALITY_LIST and next_code not in FINAL_LIST: #앞에 초성,종성,중성이 오지않을때
        result.append(SHORT_LIST_AF[code]) 

elif code in JUMP: #띄어쓰기
    result.append(JUMP[code])

elif code in NUM: # 숫자 
    if next_code in NUM_LIST:
        result.append(NUM_LIST[next_code])
        del input_data[i+1]  # NUM_LIST의 다음 코드를 리스트에서 삭제합니다.
