from nltk.stem.snowball import SnowballStemmer
import re
import math
import copy
import os


def make_stopword_list(f_name):
    f = open(f_name)
    for stopword in f:
        stopword_list = stopword.split(' ')
    return stopword_list

#delete stopword(s) in word list
def delete_stopword(word_list, stopword_list):
    for i in range(len(stopword_list)):
        if stopword_list[i] in word_list:
            word_list.remove(stopword_list[i])
    return


def UseStemmer(word_list,stemmer_obj):
    word_cnt = len(word_list)-2
    for i in range(1,word_cnt+1):
        word_list[i] = stemmer_obj.stem(word_list[i])
    return

def delete_word(complete_dic, word_dic):
    acq_word_list = word_dic['acq']
    etc_word_list = word_dic['etc']
    delete_acq_word = []
    delete_etc_word = []

    acq_word_cnt_dic = complete_dic['acq']
    etc_word_cnt_dic = complete_dic['etc']

    #delete from cnt_dic
    for word in acq_word_list:
        if acq_word_cnt_dic[word] < 5:
            delete_acq_word.append(word)
            acq_word_cnt_dic.pop(word)

    for word in etc_word_list:
        if etc_word_cnt_dic[word] < 5:
            delete_etc_word.append(word)
            etc_word_cnt_dic.pop(word)

    #delete form word_list
    for word in acq_word_list:
        if word in delete_acq_word:
            acq_word_list.pop(word)

    for word in etc_word_list:
        if word in delete_etc_word:
            etc_word_list.pop(word)
    return

def make_word_dic(file_name, stemmer, stopword_list):
    word_dic = {}

    f = open(file_name)

    for line in f:
        line_list = re.split('\t| ', line)
        delete_stopword(line_list, stopword_list)
        UseStemmer(line_list, stemmer)
        if line_list[0] == 'acq':
            input_class = line_list[0]
        else:
            input_class = 'etc'
        word_cnt = len(line_list) - 2
        # Check input_class is in input_dic
        if input_class not in word_dic:
            word_dic[input_class] = []

        word_list = word_dic[input_class]
        for i in range(1, word_cnt + 1):
            input_word = line_list[i]
            if input_word in word_list:
                continue
            else:
                word_list.append(input_word)
    return word_dic

def combine_two_word_list(word_list1, word_list2):
    new_word_list = copy.deepcopy(word_list1)
    for word2 in word_list2:
        if word2 not in new_word_list:
            new_word_list.append(word2)
    return new_word_list

def make_word_list(complete_word_dic):
    acq_word_list = complete_word_dic['acq']
    etc_word_list = complete_word_dic['etc']
    new_word_list =  combine_two_word_list(acq_word_list,etc_word_list)
    return new_word_list

def make_output_dictionary(file_name, stemmer, stopword_list ):
    output_dic = {}
    f = open(file_name)
    num_of_doc = 0
    # make dictionary => {'acq' : { 'word' : 0, ... } , 'etc' : { 'word' : 0, ... } }

    for line in f:
        num_of_doc += 1
        # line list contains => first element : class , last element : newline
        line_list = re.split('\t| ', line)
        delete_stopword(line_list, stopword_list)
        UseStemmer(line_list, stemmer)
        if line_list[0] == 'acq':
            input_class = line_list[0]
        else:
            input_class = 'etc'
        word_cnt = len(line_list) - 2
        # Check input_class is in input_dic
        if input_class not in output_dic:
            output_dic[input_class] = {}

        word_list = output_dic[input_class]
        # make word in class list or increase the count
        for i in range(1, word_cnt + 1):
            input_word = line_list[i]
            if input_word in word_list:
                word_list[input_word] += 1
            else:
                word_list[input_word] = 1
    return output_dic,num_of_doc

def calc_all_value(dic,list):
    all_num = 0
    for temp in list:
        all_num += dic[temp]
    return all_num

def calc_tf_idf(word_cnt,all_acq_word_num,num_of_doc,doc_cnt):
    term_freq = word_cnt/all_acq_word_num
    inv_doc_freq = math.log(num_of_doc/doc_cnt)
    result = term_freq * inv_doc_freq
    return result

def make_doc_cnt_dic(file_name, stemmer, stopword_list,complete_word_list):
    word_doc_cnt = {}

    for word in complete_word_list:
        word_doc_cnt[word] = 0

    f = open(file_name)

    for line in f:
        line_list = re.split('\t| ', line)
        delete_stopword(line_list, stopword_list)
        UseStemmer(line_list, stemmer)
        for word in complete_word_list:
            if word in line_list:
                word_doc_cnt[word] += 1

    return word_doc_cnt


def make_tf_idf_dic(complete_dic,complete_word_dic,all_word_list,num_of_doc,doc_cnt_dic):
    output_dic = {}
    acq_cnt_dic = complete_dic['acq']
    acq_word_list = complete_word_dic['acq']
    all_acq_word_num = calc_all_value(acq_cnt_dic,acq_word_list)

    for word in all_word_list:
        if word in acq_word_list:
            output_dic[word] = calc_tf_idf(acq_cnt_dic[word],all_acq_word_num,num_of_doc,doc_cnt_dic[word])
        else:
            output_dic[word] = 0

    return output_dic

##################functions for Adaboost###################
def make_expected_val_list(file_name):
    expected_val_list = []
    f = open(file_name)

    for line in f:
        line_list = re.split('\t| ', line)
        if line_list[0] == 'acq':
            expected_val_list.append(1)
        else:
            expected_val_list.append(-1)

    return expected_val_list

def make_output_list(input_file_name):
    input_file = open(input_file_name)
    output_list = []

    for output_val in input_file:
        if float(output_val) > 0 :
            output_list.append(1)
        else:
            output_list.append(-1)

    return output_list

def init_weight_list(weight_list,num_of_data):
    for i in range(num_of_data):
        weight_list.append(1/num_of_data)
    return

def calc_sum_of_weight(expected_val_list, weight_list, output_list, num_of_data):
    sum = 0
    for i in range(num_of_data):
        sum += weight_list[i] * math.exp( (-1) * expected_val_list[i]  * output_list[i])
    return sum

def updata_weights(weight_list,expected_val_list,output_list,alpha_val,num_of_data):
    for i in range(num_of_data):
        weight_list[i] = weight_list[i] * math.exp((-1)*expected_val_list[i]*output_list[i]*alpha_val)
    return

def make_new_weight_list(input_file_name, expected_val_list, num_of_data):
    weight_list = []
    init_weight_list(weight_list,num_of_data)
    output_list = make_output_list(input_file_name)
    sum_of_weight = calc_sum_of_weight(expected_val_list, weight_list,output_list,num_of_data)
    alpha_val = math.log((1-sum_of_weight)/sum_of_weight)/2
    updata_weights(weight_list,expected_val_list,output_list,alpha_val,num_of_data)
    return weight_list

def make_new_svm_input(input_file_name,stopword_list,stemmer,output_file_name,tf_idf_dic,all_word_list,weight_list):
    input_file = open(input_file_name)
    output_file = open(output_file_name,'w')

    i = 0
    for line in input_file:
        # line list contains => first element : class , last element : newline
        output_str = ''
        line_list = re.split('\t| ', line)
        delete_stopword(line_list, stopword_list)
        UseStemmer(line_list, stemmer)
        word_cnt = len(line_list) - 2
        #extract words from line_list AND make sorted list ascending order
        temp_list = line_list[1:word_cnt+1]

        sorted_list = []
        for word in all_word_list:
            if word in temp_list:
                sorted_list.append(word)
        #make output stirng
        if line_list[0] == 'acq':
            output_str += '1'
        else:
            output_str += '-1'
        for word in sorted_list:
            index = all_word_list.index(word)+1
            if tf_idf_dic[word] == 0:
                continue
            output_str += ' '+str(index) + ':' + str(tf_idf_dic[word]*weight_list[i])
        output_str += '\n'
        output_file.write(output_str)
        i+=1
    return

def make_svm_input(input_file_name,stopword_list,stemmer,output_file_name,tf_idf_dic,all_word_list):
    input_file = open(input_file_name)
    output_file = open(output_file_name,'w')

    for line in input_file:
        # line list contains => first element : class , last element : newline
        output_str = ''
        line_list = re.split('\t| ', line)
        delete_stopword(line_list, stopword_list)
        UseStemmer(line_list, stemmer)
        word_cnt = len(line_list) - 2
        #extract words from line_list AND make sorted list ascending order
        temp_list = line_list[1:word_cnt+1]

        sorted_list = []
        for word in all_word_list:
            if word in temp_list:
                sorted_list.append(word)
        #make output stirng
        if line_list[0] == 'acq':
            output_str += '1'
        else:
            output_str += '-1'
        for word in sorted_list:
            index = all_word_list.index(word)+1
            if tf_idf_dic[word] == 0:
                continue
            output_str += ' '+str(index) + ':' + str(tf_idf_dic[word])
        output_str += '\n'
        output_file.write(output_str)
    return

def test_exec(output_f_name1,output_f_name2,expected_list,alpha1,alpha2,len):
    output_list1 = make_output_list(output_f_name1)
    output_list2 = make_output_list(output_f_name2)
    true_num = 0
    for i in range(len):
        new_output = output_list1[i] * alpha1 + output_list2[i] * alpha2
        if (new_output > 0):
            new_output = 1
        else:
            new_output = -1
        if new_output == expected_list[i]:
            true_num += 1

    print('success rate : ' + (str)(true_num/len))



##################################MAIN###################################
alpha1 = 0
alpha2 = 0
#make stemmer object and stopword list
stemmer = SnowballStemmer("english", ignore_stopwords=False)
stop_word_f_name = 'stopword.txt'
stopword_list = make_stopword_list(stop_word_f_name)

#make word list from train set, tf*idf dictionay => {word1 : 0.xxxx, word2 : 0.xxxx, word3 : 0.xxxx, ....}
train_input_f_name = 'train.txt'
complete_output_dic,num_of_doc = make_output_dictionary(train_input_f_name,stemmer,stopword_list)
complete_word_dic = make_word_dic(train_input_f_name,stemmer,stopword_list)
complete_word_list = make_word_list(complete_word_dic)
doc_cnt_dic = make_doc_cnt_dic(train_input_f_name,stemmer,stopword_list,complete_word_list)
tf_idf_dic = make_tf_idf_dic(complete_output_dic,complete_word_dic,complete_word_list,num_of_doc,doc_cnt_dic)

#make expected value list
expected_val_list = make_expected_val_list(train_input_f_name)
#make output files
first_output_name = 'input1.txt'
second_output_name = 'input2.txt'

output_f1_name = 'output1.txt'
output_f2_name = 'output2.txt'
weight_list = []
init_weight_list(weight_list,len(expected_val_list))
make_new_svm_input(train_input_f_name,stopword_list,stemmer,first_output_name,tf_idf_dic,complete_word_list,weight_list)
print('################### model1 생성 ######################')
os.system("./svm_learn input1.txt model1.txt")
os.system("./svm_classify input1.txt model1.txt "+ output_f1_name)
new_weight_list = make_new_weight_list(output_f1_name,expected_val_list,len(expected_val_list))
make_new_svm_input(train_input_f_name,stopword_list,stemmer,second_output_name,tf_idf_dic,complete_word_list,new_weight_list)
print('################### model2 생성 ######################')
os.system("./svm_learn input2.txt model2.txt")
os.system("./svm_classify input1.txt model2.txt "+ output_f2_name)

#expected_val_list2 = make_expected_val_list('test.txt')
'''
test_input_f_name = 'test.txt'
test_output_f_name = 'new_test.txt'
output_f_name = 'output.txt'
make_new_svm_input(test_input_f_name,stopword_list,stemmer,test_output_f_name,tf_idf_dic,complete_word_list,new_weight_list)
make_new_svm_input(test_input_f_name,stopword_list,stemmer,test_output_f_name,tf_idf_dic,complete_word_list,new_weight_list)

'''

