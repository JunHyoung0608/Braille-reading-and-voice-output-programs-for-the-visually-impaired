INITIAL_LIST = {8: 'ㄱ', 9: 'ㄴ', 10: 'ㄷ', 16: 'ㄹ', 17: 'ㅁ', 24: 'ㅂ', 32: 'ㅅ', 40: 'ㅈ', 48: 'ㅊ', 11: 'ㅋ', 19: 'ㅌ', 25: 'ㅍ', 26: 'ㅎ'}
NEUTRALITY_LIST = {35: 'ㅏ', 28: 'ㅑ', 14: 'ㅓ', 49: 'ㅕ', 37: 'ㅗ', 44: 'ㅛ', 13: 'ㅜ', 41: 'ㅠ', 42: 'ㅡ', 21: 'ㅣ', 23: 'ㅐ', 29: 'ㅔ', 12: 'ㅖ', 39: 'ㅘ', 61: 'ㅚ', 15: 'ㅝ', 58: 'ㅢ'}
FINAL_LIST = {1: 'ㄱ', 18: 'ㄴ', 20: 'ㄷ', 2: 'ㄹ', 34: 'ㅁ', 3: 'ㅂ', 4: 'ㅅ', 54: 'ㅇ', 5: 'ㅈ', 6: 'ㅊ', 22: 'ㅋ', 38: 'ㅌ', 50: 'ㅍ', 52: 'ㅎ', 12: 'ㅆ'}
AND_LIST = {14: '그래서', 9: '그러나', 18: '그러면', 34: '그러므로', 29: '그런데', 37: '그리고', 49: '그리하여'}
NUM_LIST = {1: '1', 3: '2', 9: '3', 25: '4', 17: '5', 11: '6', 27: '7', 19: '8', 10: '9', 26: '0'}
SHORT_LIST = {43: '가', 9: '나', 10: '다', 17: '마', 24: '바', 7: '사', 40: '자', 11: '카', 19: '타', 25: '파', 26: '하', 57: '억', 62: '언', 30: '얼', 33: '연', 51: '열', 59: '영', 45: '옥', 55: '온', 63: '옹', 27: '운', 47: '울', 53: '은', 46: '을', 31: '인'}
PASS_LIST = [0]

def find_lists_and_conditions(numbers):
    results = []
    for number in numbers:
        lists = {}

        if number in INITIAL_LIST and number in NEUTRALITY_LIST and number in FINAL_LIST:
            lists["INITIAL_LIST"] = True
            lists["NEUTRALITY_LIST"] = True
            lists["FINAL_LIST"] = True

        if number in INITIAL_LIST and number in NEUTRALITY_LIST:
            lists["INITIAL_LIST"] = True
            lists["NEUTRALITY_LIST"] = True

        if number in SHORT_LIST:
            idx = list(SHORT_LIST.keys()).index(26)
            if idx != 0 and number == 26 and list(SHORT_LIST.keys())[idx - 1] in FINAL_LIST:
                lists["FINAL_LIST"] = True

        if number in INITIAL_LIST and number in SHORT_LIST and 26 in SHORT_LIST:
            lists["INITIAL_LIST"] = True
            lists["SHORT_LIST"] = True

        if number == 1 and number in AND_LIST:
            lists["AND_LIST"] = True

        if number == 60 and number in NUM_LIST:
            lists["NUM_LIST"] = True

        # 결과에 추가
        if any(lists.values()):  # 하나 이상의 조건이 True인 경우에만 결과에 추가
            results.append(lists)

    return results

# 예시 입력
input_data_str = "9,20,9,42,18,0,26,23,54,0,24,45,26,3,9,21,10,60,17"
input_data = [int(x) for x in input_data_str.split(',')]

# 결과 출력
print(find_lists_and_conditions(input_data))
