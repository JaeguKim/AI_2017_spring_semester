from nltk.stem.snowball import SnowballStemmer
import re
import math
import operator

#parameter => file name, stemmer obj, stopword_list
#return complete_dictionary,class name list, number of class, class count dictionary
def make_dictionary(file_name, stemmer, stopword_list ):
    input_dic = {}
    cnt_in_class = {}
    class_name_list = []
    f = open(file_name)
    num_of_class = 0
    num_of_training_data = 0
    # make dictionary => {'earn' : { 'word' : 0, ... } , ... }

    for line in f:
        num_of_training_data += 1
        # line list contains => first element : class , last element : newline
        line_list = re.split('\t| ', line)
        delete_stopword(line_list, stopword_list)
        UseStemmer(line_list, stemmer)
        input_class = line_list[0]
        word_cnt = len(line_list) - 2
        # Check input_class is in input_dic
        if input_class not in input_dic:
            input_dic[input_class] = {}
            num_of_class+=1
            cnt_in_class[input_class] = 1
            class_name_list.append(input_class)
        else:
            cnt_in_class[input_class] += 1

        word_list = input_dic[input_class]
        # make word in class list or increase the count
        for i in range(1, word_cnt + 1):
            input_word = line_list[i]
            if input_word in word_list:
                word_list[input_word] += 1
            else:
                word_list[input_word] = 1
    return input_dic, cnt_in_class,num_of_class,class_name_list, num_of_training_data

#parameter =>  file_name, complete dictionary form training set, class name lsit, class probability list, stemmer obj, stopword list
#return => number of test data, success rate from test set
def exec_test(file_name,input_dic,class_name_list,class_prob_dic,stemmer,stopword_list):
    f = open(file_name)
    all_num = 0
    true_num = 0
    num_of_test_data = 0

    for line in f:
        num_of_test_data += 1
        all_num += 1
        # line list contains => first element : class , last element : newline
        line_list = re.split('\t| ', line)
        delete_stopword(line_list, stopword_list)
        UseStemmer(line_list, stemmer)
        true_class = line_list[0]
        answer = calc_answer(input_dic, class_name_list, class_prob_dic, line_list)
        if answer == true_class:
            true_num += 1
    success_rate = true_num/all_num
    return num_of_test_data,success_rate


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


def make_class_prob_dic(cnt_class_dic, class_list):
    class_prob_dic = {}
    num_of_input = sum(cnt_class_dic.values())

    for class_name in class_list:
        class_prob_dic[class_name] = cnt_class_dic[class_name]/num_of_input

    return class_prob_dic


def calc_BayesClassifier(word_cnt_info, class_name, class_prob_dic, input_list):
    input_word_cnt = len(input_list) - 2
    log_sum = 0
    temp_word_cnt_dic = {}
    temp_word_list = []
    zero_cnt = 0

    #count zero count in input list if word is not in complete_word_dic, save word and word count to temp_dic
    for i in range(1,input_word_cnt+1):
        temp_word_list.append(input_list[i]) #append word
        if input_list[i] in word_cnt_info.keys():
            temp_word_cnt_dic[input_list[i]] = word_cnt_info[input_list[i]]
        else:
            temp_word_cnt_dic[input_list[i]] = 1
            zero_cnt += 1

    #calculate log summation
    for temp_word in temp_word_list:
        numerator = temp_word_cnt_dic[temp_word]
        denominator = sum(word_cnt_info.values()) + zero_cnt #분모에 zero개수 만큼 더해준다
        log_sum += math.log10(numerator/denominator)
    result = math.log10(class_prob_dic[class_name]) + log_sum
    return result


def calc_answer(complete_word_dic, class_name_list, class_prob_dic, input_list):
    BayesClassifier_dic = {}
    for class_name in class_name_list:
        BayesClassifier_dic[class_name] = calc_BayesClassifier(complete_word_dic[class_name],class_name,class_prob_dic,input_list)
    answer = max(BayesClassifier_dic.items(), key=operator.itemgetter(1))[0]
    return answer


def make_stopword_list(f_name):
    f = open(f_name)
    for stopword in f:
        stopword_list = stopword.split(' ')
    return stopword_list



###################################MAIN###################################
#make stemmer object and stopword list
stemmer = SnowballStemmer("english", ignore_stopwords=False)
f_name = 'stopword.txt'
stopword_list = make_stopword_list(f_name)

######training#####
f_name = 'train.txt'
input_dic,cnt_in_class,num_of_class,class_name_list,num_of_training_data = make_dictionary(f_name,stemmer,stopword_list)
class_prob_dic = make_class_prob_dic(cnt_in_class,class_name_list)

######testing#####
f_name = 'test.txt'
num_of_test_data, success_rate = exec_test(f_name,input_dic,class_name_list,class_prob_dic,stemmer,stopword_list)

print('##############test################')
print('num of training data : '+str(num_of_training_data))
print('num of test data : '+str(num_of_test_data))
print('Success Rate : ' + str(success_rate))
