
def func_word(result_dic, words):
    for word in words:
        if word in result_dic:
            result_dic[word]+=1
        else:
            result_dic[word] = 1


def find_max_in_dic(result_dic):
    max = -1
    str = ''
    result_str = []
    result_str2 = []
    for key in result_dic:
        if result_dic[key] > max:
            max = result_dic[key]

    for key in result_dic:
        if result_dic[key] == max:
            result_str.append(key)
            result_str2.append(result_dic[key])
    return result_str, result_str2


file_name = input('파일명을 입력하세요 : ')
file_obj = open(file_name, 'r')
list = []
word_cnt = 0
line_cnt = 0
word_dic = {}
word_cnt_dic = {}

for line in file_obj:
    temp_word_list = line.split()
    func_word(word_dic, temp_word_list )
    word_cnt += len(temp_word_list)
    line_cnt += 1
    word_cnt_dic[line_cnt] = len(temp_word_list)

print('단어수 : ' + str(word_cnt))
print('줄수 : ' + str(line_cnt))

max_word_list, temp = find_max_in_dic(word_dic)
max_word_str= ''.join(max_word_list)
print('가장 많이 쓰인 단어 : ' + max_word_str)

temp_str1, temp_str2 = find_max_in_dic(word_cnt_dic)
max_line_num = ', '.join(str(x) for x in temp_str1)
max_word_num = ', '.join(str(x) for x in temp_str2)
print('단어가 가장 많은 라인 : ' + max_line_num)
print('단어가 가장 많이 포함된 라인에서의 단어수 : ' + max_word_num)