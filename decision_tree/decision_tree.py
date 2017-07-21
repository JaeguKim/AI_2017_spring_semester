import numpy as np
import copy
from collections import OrderedDict

class Node:
    data = ''

    def __init__(self):
       self.child_dic = {}
       self.attr_list = []

    def print_child_dic(self): #child_dic를 만들고, attr_list도 만든다
        print(self.child_dic)

    def set_child_dic(self,attr_list):
        for temp in attr_list:
            self.child_dic[temp] = Node()
            self.attr_list.append(temp)

    def get_child_dic(self):
        return self.child_dic

    def print_nodes(self):
        if self.data == 'empty':
            print('empty')
            return
        print(self.data)
        if self.data is 'e' or self.data is 'p': #terminal node이면 return
            return
        for temp in self.attr_list:
            print(str(temp) + '일때')
            self.child_dic[temp].print_nodes()


def calc_antrophy(list):
    e_num = 0
    p_num = 0
    for temp in list:
        if temp['classes'] == 'e':
            e_num = e_num+1
        elif temp['classes'] == 'p':
            p_num = p_num+1
    all_num = e_num + p_num
    result = (-1) * (e_num/all_num) * np.log2(e_num/all_num) + (-1) * (p_num/all_num) * np.log2(p_num/all_num)
    return result


def calc_antrophy2(list):
    e_num = list[0]
    p_num = list[1]
    all_num = e_num + p_num
    if e_num == 0 and p_num == 0:
        return 0
    elif e_num == 0 and p_num != 0:
        result = (-1) * (p_num / all_num) * np.log2(p_num / all_num)
        return result
    elif p_num == 0 and e_num != 0:
        result = (-1) * (e_num / all_num) * np.log2(e_num / all_num)
        return result
    result = (-1) * (e_num / all_num) * np.log2(e_num / all_num) + (-1) * p_num / all_num * np.log2(p_num / all_num)
    return result


def calc_gain(total_entrophy, total_num, temp, dic_name, ent_list, attr_array):
    result = total_entrophy
    for i in dic_name[temp]:
        result -= (attr_array[temp][i][0] + attr_array[temp][i][1])/total_num * ent_list[temp][i]
    return result


def all_same(items): #list안에 값들이 서로 같은지 검사하는 함수
    return all(x == items[0] for x in items)


def check_end(training_dic_list, attr_name_list): #끝인경우는 true를 반환 끝이 아닌경우는 false
    #attrbute_name_list에 아무것도 없는 경우 or e,p값이 섞여있지 않은경우
    if (len(attr_name_list) == 1):  #classes 항목만 남아있는경우(가지가 모두 뻣어나간경우
        #print("List is empty!")
        return True
    #e,p 값 섞여있는지 판단
    result_list = []
    for temp in training_dic_list:
        result_list.append(temp['classes'])
    if all_same(result_list) is True:
        return True
    return False


def make_decision_tree(root_node,training_dic_list,attr_name_list,dic_name,copy_training_dic_list,cur_attr_name,cur_branch_val):

    if not training_dic_list: #training_dic_list에 아무값도 없는경우(특정값을 가지는 데이터가 없는경우)
        #print('empty node')
        #root_node.data = 'empty'
        temp_node = make_empty_terminal_node(copy_training_dic_list,cur_attr_name,cur_branch_val)
        root_node.data = temp_node.data
        return

    if check_end(training_dic_list,attr_name_list) is True: #종료조건
        #terminal node를 등록
        temp_node = make_terminal_node(training_dic_list,attr_name_list)
        root_node.data = temp_node.data
        return

    total_num = len(training_dic_list)
    #print('total_num : ' + str(total_num))
    D = calc_antrophy(training_dic_list)
    #print('D : '+str(D))
    # 2) 22개의 attr 각각에 대한 Gain값 계산
    attr_list = {}
    attr_temp1 = {}

    attr_ent = {}
    attr_temp2 = {}

    gain_list = {}

    for attr_name in attr_name_list[1:]:
        for j in dic_name[attr_name]:
            attr_temp1[j] = [0, 0]
            attr_temp2[j] = 0
        attr_list[attr_name] = attr_temp1
        attr_ent[attr_name] = attr_temp2
        gain_list[attr_name] = 0
        attr_temp1 = {}
        attr_temp2 = {}

    # e,p 구분
    for line in training_dic_list:
        for temp in attr_name_list[1:]:
            if line['classes'] == 'e':
                attr_list[temp][line[temp]][0] += 1
            elif line['classes'] == 'p':
                attr_list[temp][line[temp]][1] += 1

    # entrophy 계산
    for temp in attr_name_list[1:]:
        for temp2 in dic_name[temp]:
            attr_ent[temp][temp2] = calc_antrophy2(attr_list[temp][temp2])

    # gain 값 구하기
    for temp in attr_name_list[1:]:
        gain_list[temp] = calc_gain(D, total_num, temp, dic_name, attr_ent, attr_list)

    # gain이 최대인 칼럼찾기
    max_attr_name = max(gain_list, key=gain_list.get)
    #print('max_attr_name')
    #print(max_attr_name)
    # 최대인 칼럼으로 노드생성 => attribute 종류만큼 child node 생성
    #root_node = Node(max_attr_name,dic_name[max_attr_name])
    root_node.data = max_attr_name
    root_node.set_child_dic(dic_name[max_attr_name])
    #print('child_dic')
    #root_node.print_child_dic()

    new_attribute_name_list = make_new_attribute_name_list(attr_name_list, max_attr_name)

    #training data set 가공
    for temp in dic_name[max_attr_name]:
        new_training_data_list = make_new_training_data_list(training_dic_list,max_attr_name,temp)
        make_decision_tree(root_node.child_dic[temp],new_training_data_list,new_attribute_name_list,dic_name,copy_training_dic_list,max_attr_name,temp)

    return root_node

def make_empty_terminal_node(copy_training_dic_list,cur_attr_name,cur_branch_val):
    result_list = []

    for temp in copy_training_dic_list:
        if temp[cur_attr_name] == cur_branch_val:
            result_list.append(temp['classes'])

    '''
    if (len(result_list) == 0): #오리지날 데이타 셋에서도 대응값이 없음 => empty node로 생성
        terminal_node = Node()
        terminal_node.data = 'empty'
        return terminal_node
    '''
    print('training_dic_list에서 현재 해당값이 없음, 오리지날 데이터셋에서 다수결로 결정')
    if result_list.count('e') >= result_list.count('p'):  # result_set에서 더 많은 값으로 선택
        terminal_node = Node()
        terminal_node.data = 'e'
    else:
        terminal_node = Node()
        print('cur_branch_val : '+cur_branch_val)
        print(result_list)
        print(len(result_list))
        terminal_node.data = 'p'
    return terminal_node

def make_terminal_node(training_dic_list,attr_name_list):#training_dic_list 값이 들어있는 경우 호출
    #결과값 모두 저장
    result_list = []

    for temp in training_dic_list:
        result_list.append(temp['classes'])

    if len(attr_name_list) == 1: #attr_name_list가 비어있는경우
        if all_same(result_list) is True:  # attr_name_list에 아무것도 없으면서(끝까지 가지를 뻗은경우) 값이 모두 동일한 경우
            #terminal_node = Node(result_list[0])
            terminal_node = Node()
            terminal_node.data = result_list[0]
            #print("List is empty and all value is same!")
        elif all_same(result_list) is False:  # attr_name_list에 아무것도 없으면서(끝까지 가지를 뻗은경우) 값이 섞여있는 경우
            #print("terminal에서 다수결로 결정")
            # result_set에서 더 많은 값으로 선택
            if result_list.count('e') >= result_list.count('p'):
                terminal_node = Node()
                terminal_node.data = 'e'
            else:
                terminal_node = Node()
                terminal_node.data = 'p'
    else: #attr_name_list에 값이 있지만 결과값이 모두 동일한 경우
        #print('NOT empty')
        terminal_node = Node()
        terminal_node.data = result_list[0]
        #print("List is NOT empty BUT all value is same!")

    return terminal_node


def make_new_training_data_list(training_data_list, attr_name, value): #value와 일치하는 값을 가지는 데이터셋만 찾아서 반환
    new_training_data_list = []
    for temp in training_data_list:
        if temp[attr_name] == value:
            new_training_data_list.append(temp)
    return new_training_data_list


def make_new_attribute_name_list(attr_name_list,attr_name):
    for i in range(len(attr_name_list)):
        if attr_name_list[i] == attr_name:
            attr_name_list.pop(i)
            return attr_name_list


def func_test_data(root_node, test_dic_list):
    all_num = len(test_dic_list)
    correct_num = 0
    wrong_num = 0

    for test_dic in test_dic_list: #총 데이터의 수만큼 반복
        temp_node = root_node
        #print(temp_node.data)
        while is_terminal(temp_node.data) is False: #terminal이 될때 까지 반복
            #print('node_data')
            node_data = test_dic[temp_node.data]
            #print(node_data)
            temp_node = temp_node.child_dic[node_data]

        if (temp_node.data == test_dic['classes']):
            correct_num+=1
        else:
            #print('result : ' + temp_node.data)
            #print('real value : ' + test_dic['classes'])
            wrong_num+=1


    suc_percent = (correct_num/all_num) * 100
    fail_percent = (wrong_num/all_num) * 100

    print('correct_num : ' + str(correct_num))
    print('wrong num : ' + str(wrong_num))
    print('success percentage : ' + str(suc_percent))
    print('fail percentage : ' + str(fail_percent))


def is_terminal(data):
    if data == 'e' or data == 'p' or data == 'empty':
        return True
    return False

#################################################################
#mushroom.names file 읽어서, dictionary에 저장 eg.  { 'classes' : {e,p}, ....}
file_msuhroom_names = open("mushroom.names",'r')
dic_name = OrderedDict()
for line in file_msuhroom_names:
    temp = line.split(' ')
    attr_values = []
    for item in temp[1:]:
        attr_values.append(item.strip('\n'))
    dic_name[temp[0]] = attr_values
print('dic_name')
print(dic_name)
#attr name을 저장
items = list(dic_name.items())
attr_name_list = []
for temp in items:
    attr_name_list.append(temp[0])
print('attr_name_list')
print(attr_name_list)

#training data를 파일로 부터 읽어서 dictionary 형태로 변환
#training_data = open('training_set.txt','r')
training_data = open('xxx.data.txt','r')
#training_data = open('a.txt','r')

training_dic_list = []

for line in training_data:
    temp1 = line.split(',')
    i = 0
    training_dic = {}
    for temp2 in attr_name_list:
        training_dic[temp2] = temp1[i].strip('\n')
        i+=1
    training_dic_list.append(training_dic)

copy_training_dic_list = copy.deepcopy(training_dic_list)

print('********************************************')
new_attr_name_list = copy.deepcopy(attr_name_list)
root_node = Node()
root_node = make_decision_tree(root_node,training_dic_list,new_attr_name_list, dic_name,copy_training_dic_list,'',0)
print('*********************************************')

print('***************트리출력*****************')
root_node.print_nodes()

#test_data = open('test_set.txt','r')
#test_data = open('new_test_set.txt','r')
#test_data = open('validation_set.txt','r')
#test_data = open('b.txt','r')
#test_data = open('input.txt','r')
test_data = open('xxx.test.txt','r')

test_dic_list = []
for line in test_data:
    temp1 = line.split(',')
    i = 0
    test_dic = {}
    for temp2 in attr_name_list:
        test_dic[temp2] = temp1[i].strip('\n')
        i+=1
    test_dic_list.append(test_dic)

func_test_data(root_node,test_dic_list)
