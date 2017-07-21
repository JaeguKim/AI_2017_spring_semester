import random
import math

def sigmoid(x):
  return 1 / (1 + math.exp(-x))

def calc_output(x_list,w_list):
    result = 0
    for i in range(len(x_list)):
        result = result + x_list[i]*w_list[i]
    result = sigmoid(result)
    return result

def calc_real_output(x_list,w_list):
    result = 0
    for i in range(len(x_list)):
        result = result + x_list[i] * w_list[i]
    return result

def calc_output_delta(target, output_val):
    result = output_val * (1-output_val) * (target - output_val)
    return result

def calc_hidden_delta(output_percept_dic,output_delta_dic,hidden_node_num, output_val):
    sum = 0
    for i  in range(10):
        sum += output_delta_dic[i]*output_percept_dic[i][hidden_node_num]
    result = output_val * (1-output_val)*sum
    return result

#output layer에서 output node 한개에 대한 w_list 수정
def change_w_list_output(w_list,x_list,learning_rate,target,output):
    for i in range(len(w_list)):
        w_list[i] = w_list[i] + learning_rate*calc_output_delta(target,output)*x_list[i]
    return

#hidden layer에서 hidden node 한개에 대한 w_list 수정
def change_w_list_hidden(hidden_w_list,learning_rate,hidden_delta_val,x_list):
    for i in range(len(hidden_w_list)):
        hidden_w_list[i] = hidden_w_list[i] + learning_rate*hidden_delta_val*x_list[i]
    return


learning_rate = 0.05
#output layer, hidden layer 선언
output_percept_dic = {0 : [], 1 : [], 2 : [], 3 : [], 4 : [], 5 : [], 6 : [], 7 : [], 8 : [], 9 : []}
hidden_percept_dic = {0 : [], 1 : [], 2 : [], 3 : [], 4 : [], 5 : [], 6 : [], 7 : [], 8 : [], 9 : []}
output_delta_dic = {0 : 0, 1 : 0, 2 : 0, 3 : 0, 4 : 0, 5 : 0, 6 : 0, 7 : 0, 8 : 0, 9 : 0}
hidden_delta_dic = {0 : 0, 1 : 0, 2 : 0, 3 : 0, 4 : 0, 5 : 0, 6 : 0, 7 : 0, 8 : 0, 9 : 0}

for i in range(10):
    for j in range(10):
        output_percept_dic[j].append(random.uniform(-0.125,0.125))

for i in range(10):
    for j in range(65):
        hidden_percept_dic[i].append(random.uniform(-0.125,0.125))

training_data = open('optdigits.tra','r')
#training_data = open('a.txt','r')

for i in range(50):
    training_data = open('optdigits.tra', 'r')
    for line in training_data:
        output_layer_output = []
        hidden_layer_output = []
        x_list = [1]
        temp_list = line.split(',')
        for i in range(64):
            x_list.append(int(temp_list[i]))
        target_val = int(temp_list[64])
        #Forward Propagation
        for i in range(10):
            hidden_layer_output.append(calc_output(x_list,hidden_percept_dic[i]))
        for i in range(10):
            output_layer_output.append(calc_output(hidden_layer_output,output_percept_dic[i]))
        #Backward Propagation
        #output layer w값수정
        for i in range(10):
            if target_val == i:
                change_w_list_output(output_percept_dic[i],hidden_layer_output,learning_rate,1,output_layer_output[i])
                # output_delta 값 구하기
                output_delta_dic[i] = calc_output_delta(1, output_layer_output[i])
            else:
                change_w_list_output(output_percept_dic[i], hidden_layer_output, learning_rate, 0, output_layer_output[i])
                #output_delta 값 구하기
                output_delta_dic[i] = calc_output_delta(0, output_layer_output[i])

        #hidden layer의 delta값 구하기
        for i in range(10):
            hidden_delta_dic[i] = calc_hidden_delta(output_percept_dic,output_delta_dic,i,hidden_layer_output[i])

        #hidden layer w값수정
        for i in range(10):
            change_w_list_hidden(hidden_percept_dic[i],learning_rate,hidden_delta_dic[i],x_list)

print('output layer:')
for i in range(10):
    print(i)
    print(output_percept_dic[i])

print('hidden layer:')
for i in range(10):
    print(i)
    print(hidden_percept_dic[i])


test_data = open('optdigits.tes','r')
#test_data = open('b.txt','r')

correct_num = 0
wrong_num = 0
result_dic = {0 : 0 , 1 : 0, 2 : 0, 3 : 0, 4 : 0, 5: 0, 6 : 0, 7 : 0, 8 : 0, 9 : 0}

print('####### test #######')
for line in test_data:
    hidden_layer_output = []
    x_list = [1]
    temp_list = line.split(',')
    for i in range(64):
        x_list.append(int(temp_list[i]))

    #hidden_layer_output 생성
    for i in range(10):
        hidden_layer_output.append(calc_output(x_list,hidden_percept_dic[i]))
    #output_layer_output 생성 -> result_dic에 저장
    for i in range(10):
        result_dic[i] = calc_output(hidden_layer_output,output_percept_dic[i])

    #answer = min(result_dic, key=lambda key: result_dic[key])
    answer = max(result_dic, key=lambda key: result_dic[key]) #값중에서 최대값을 구함
    #print(answer)
    #print('답 : ' + str(answer))
    true_num = int(temp_list[64])
    if answer == true_num:
        print(true_num)
        print(result_dic)
        correct_num = correct_num+1
    else:
        #print('wrong')
        #print(result_dic)
        wrong_num = wrong_num+1

all_num = correct_num + wrong_num
success_percent = correct_num/all_num * 100
fail_percent = wrong_num/all_num * 100
print('Success Percent :' + str(success_percent))
print('Failure Percent :' + str(fail_percent))
#print(w_list)
