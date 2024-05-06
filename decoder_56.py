#5/6 11:38pm
#현재 상태
#초성: 0, 중성: 0, 종성: 0, 약자: 0, 약어 : x, 숫자: 0, 문장부호: x

INITIAL_LIST = {8: 'ㄱ', 9: 'ㄴ', 10: 'ㄷ', 16: 'ㄹ', 17: 'ㅁ', 24: 'ㅂ', 32: 'ㅅ', 40: 'ㅈ', 48: 'ㅊ', 11: 'ㅋ', 19: 'ㅌ', 25: 'ㅍ', 26: 'ㅎ'}
NEUTRALITY_LIST = {35: 'ㅏ', 28: 'ㅑ', 14: 'ㅓ', 49: 'ㅕ', 37: 'ㅗ', 44: 'ㅛ', 13: 'ㅜ', 41: 'ㅠ', 42: 'ㅡ', 21: 'ㅣ', 23: 'ㅐ', 29: 'ㅔ', 12: 'ㅖ', 39: 'ㅘ', 61: 'ㅚ', 15: 'ㅝ', 58: 'ㅢ'}
FINAL_LIST = {1: 'ㄱ', 18: 'ㄴ', 20: 'ㄷ', 2: 'ㄹ', 34: 'ㅁ', 3: 'ㅂ', 4: 'ㅅ', 54: 'ㅇ', 5: 'ㅈ', 6: 'ㅊ', 22: 'ㅋ', 38: 'ㅌ', 50: 'ㅍ', 52: 'ㅎ', 12: 'ㅆ'}
AND_LIST = {14: '그래서', 9: '그러나', 18: '그러면', 34: '그러므로', 29: '그런데', 37: '그리고', 49: '그리하여'}
NUM_LIST = {1: '1', 3: '2', 9: '3', 25: '4', 17: '5', 11: '6', 27: '7', 19: '8', 10: '9', 26: '0'}
SHORT_LIST_BE = {43: '가', 9: '나', 10: '다', 17: '마', 24: '바', 7: '사', 40: '자', 11: '카', 19: '타', 25: '파', 26: '하'}
SHORT_LIST_AF = {57: '억', 62: '언', 30: '얼', 33: '연', 51: '열', 59: '영', 45: '옥', 55: '온', 63: '옹', 27: '운', 47: '울', 53: '은', 46: '을', 31: '인'}
PASS = {0:'00'}
JUMP = {100:' '}
NUM = [60]

input_data = [9, 9, 42, 18, 100, 26, 23, 54, 0, 24, 45, 26, 3, 9, 21, 10, 60, 17,8,35,35,28,49]

result = []
prev_type = None
next_code = None

for i, code in enumerate(input_data):
    if i < len(input_data) - 1:
        next_code = input_data[i + 1]
    else:
        next_code = None

    if code in INITIAL_LIST:
        result.append(INITIAL_LIST[code])
        if next_code not in NEUTRALITY_LIST and next_code not in SHORT_LIST_AF:
            result[-1] = SHORT_LIST_BE[code]  # 단독으로 사용될 경우 SHORT_LIST_BE로 변경
            prev_type = None
        else:
            prev_type = 'INITIAL'
    elif code in NEUTRALITY_LIST:
        if prev_type != 'INITIAL':
            result.append('ㅇ')
            result.append(NEUTRALITY_LIST[code])
        else:
            result.append(NEUTRALITY_LIST[code])
        prev_type = 'NEUTRALITY'
    elif code in FINAL_LIST:
        result.append(FINAL_LIST[code])
        if next_code in NEUTRALITY_LIST or next_code in SHORT_LIST_BE or next_code in AND_LIST:
            prev_type = 'FINAL'
        else:
            prev_type = None
    elif code in AND_LIST:
        if result[-1] == '1':
            result[-1] = AND_LIST[code]
            result.append('0')
        else:
            result.append(AND_LIST[code])
        prev_type = 'AND'
    elif code in SHORT_LIST_BE:
        if next_code in FINAL_LIST:
            result.append(SHORT_LIST_BE[code])
        else:
            result[-1] += SHORT_LIST_BE[code]
        prev_type = 'SHORT_BE'
    elif code in SHORT_LIST_AF:
        if prev_type == 'INITIAL':
            result.append(SHORT_LIST_AF[code])
        else:
            result[-1] += SHORT_LIST_AF[code]
        prev_type = 'SHORT_AF'
    elif code in PASS:
        result.append(PASS[code])
    elif code in JUMP:
        result.append(JUMP[code])
    elif code in NUM:
        if next_code in NUM_LIST:
            result.append(NUM_LIST[next_code])
            input_data.pop(i + 1)  # NUM_LIST의 다음 코드를 리스트에서 삭제합니다.

print(result)
