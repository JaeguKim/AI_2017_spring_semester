import random

def calc_output(x_list,w_list):
    result = 0
    for i in range(65):
        result = result + x_list[i]*w_list[i]
    if result > 0:
        result = 1
    else:
        result = 0
    return result

def calc_output2(x_list,w_list):
    result = 0
    for i in range(65):
        result = result + x_list[i]*w_list[i]
    return result

def change_w_list(w_list,x_list,learning_rate,target,output):
    for i in range(len(w_list)):
        w_list[i] = w_list[i] + learning_rate*(target-output)*x_list[i]
    return


learning_rate = 0.1
#perceptron 초기화
percept_dic = {0 : [], 1 : [], 2 : [], 3 : [], 4 : [], 5 : [], 6 : [], 7 : [], 8 : [], 9 : []}

for i in range(65):
    percept_dic[0].append(random.uniform(0, 1))
    percept_dic[1].append(random.uniform(0, 1))
    percept_dic[2].append(random.uniform(0, 1))
    percept_dic[3].append(random.uniform(0, 1))
    percept_dic[4].append(random.uniform(0, 1))
    percept_dic[5].append(random.uniform(0, 1))
    percept_dic[6].append(random.uniform(0, 1))
    percept_dic[7].append(random.uniform(0, 1))
    percept_dic[8].append(random.uniform(0, 1))
    percept_dic[9].append(random.uniform(0, 1))

#training_data = open('a.txt','r')

for temp in range(3):
    training_data = open('optdigits.tra', 'r')
    for line in training_data:
        x_list = [1]
        temp_list = line.split(',')
        for i in range(64):
            x_list.append(int(temp_list[i]))
        target_val = int(temp_list[64])
        #output_val = calc_output(calc_output(x_list,percept_dic[target_val])) #target value 값과 같은 perceptron 에 대한 output 계산
        for i in range(10): #0~9까지의 perceptron에 대하여
            if i == target_val:
                output_val = calc_output(x_list,percept_dic[i])
                change_w_list(percept_dic[i],x_list,learning_rate,1,output_val) #해당 perceptron만 1로 학습
            else:
                output_val = calc_output(x_list,percept_dic[i])
                change_w_list(percept_dic[i], x_list, learning_rate, 0, output_val) #나머지 perceptron은 0으로 학습

for i in range(10):
    print(percept_dic[i])

test_data = open('optdigits.tes','r')
#test_data = open('b.txt','r')

correct_num = 0
wrong_num = 0
result_dic = {0 : 0 , 1 : 0, 2 : 0, 3 : 0, 4 : 0, 5: 0, 6 : 0, 7 : 0, 8 : 0, 9 : 0}

for line in test_data:
    x_list = [1]
    temp_list = line.split(',')
    for i in range(64):
        x_list.append(float(temp_list[i]))
    for i in range(10):
        #result_dic[i] = 1 - calc_output(x_list,percept_dic[i])
        result_dic[i] = calc_output2(x_list, percept_dic[i])
    print(result_dic)
    #answer = min(result_dic, key=lambda key: result_dic[key])
    answer = max(result_dic, key=lambda key: result_dic[key])

    #print('답 : ' + str(answer))
    true_num = int(temp_list[64])
    if answer == true_num:
        #print('correct')
        correct_num = correct_num+1
    else:
        #print('wrong')
        #print(result_dic)
        #print(answer)
        #print(true_num)
        wrong_num = wrong_num+1

all_num = correct_num + wrong_num
success_percent = correct_num/all_num * 100
fail_percent = wrong_num/all_num * 100
print('Success Percent :' + str(success_percent))
print('Failure Percent :' + str(fail_percent))
#print(w_list)
