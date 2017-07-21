from __future__ import unicode_literals, print_function

import pycrfsuite

def index2feature(sent, i, offset): #index 정보를 첨가하여 string 반환
    word, tag = sent[i + offset]
    if offset < 0:
        sign = ''
    else:
        sign = '+'
    return '{}{}:word={}'.format(sign, offset, word)

def word2features(sent, i): #현재 형태소 앞에 2개와 뒤에 2개정보를 첨가하여 리스트로 반환
    L = len(sent)
    word, tag = sent[i]
    features = ['bias']
    features.append(index2feature(sent, i, 0))

    if i > 1:
        features.append(index2feature(sent, i, -2))
    if i > 0:
        features.append(index2feature(sent, i, -1))
    else:
        features.append('bos')

    if i < L - 2:
        features.append(index2feature(sent, i, 2))
    if i < L - 1:
        features.append(index2feature(sent, i, 1))
    else:
        features.append('eos')
    return features

def sent2tags(sent):
    return [tag for word, tag in sent]

def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]

def inputToList(f_name,true_list): #train.txt를 읽어서 정답리스트와 [형태소,태그] 리스트 생성
    input_f = open(f_name, 'r', encoding='utf-8')
    total_sentence = []

    for line in input_f: #한줄씩 읽기
        if (line == '\n'): #개행이면 무시
            continue
        word,tags = line.split(' ')
        tags = tags.rstrip() # \n제거
        #print(tags)
        if '+' in tags: #'+'문자 기준으로 나누기
            tags = tags.split('+')
            sentences1 = []
            temp_sentence = []
            for temp2 in tags:
                sentence = []
                if temp2[0] == '/': #첫문자가 '/' 인경우
                    temp_word = '/'
                    temp_tag = temp2[2:]
                else:
                    temp_word, temp_tag = temp2.split('/')
                sentence.append(temp_word)
                temp_sentence.append(temp_tag)
                sentence.append(temp_tag)
                sentences1.append(sentence)
            total_sentence.append(sentences1)
            true_list.append(temp_sentence)
        else: #'+' 없는경우(그 자체가 하나의 형태소인경우)
            sentence = []
            sentences1 = []
            temp_sentence = []
            if tags[0] == '/': #첫문자가 '/' 인경우
                temp_word = '/'
                temp_tag = tags[2:]
            else:
                temp_word, temp_tag = tags.split('/')
            temp_sentence.append(temp_tag)
            sentence.append(temp_word)
            sentence.append(temp_tag)
            sentences1.append(sentence)
            total_sentence.append(sentences1)
            true_list.append(temp_sentence)

    return total_sentence #전체 [형태소, 태그] 리스트 반환

def test_result(list1,list2):
    print('******test******')
    all_num = len(list1) #전체 항목갯수
    true_num = 0 #맞은 갯수
    for i in range(all_num):
        if list1[i] == list2[i]: #두 태깅 결과가 일치
            true_num += 1 #맞은 갯수 카운트 +1
    success_rate = true_num/all_num #정답률 계산
    print('Success Rate : '+str(success_rate))


true_list = [] #정답을 저장할 리스트
train_sents = inputToList('train.txt',true_list) #train.txt를 읽어서 [형태소,태그]들의 리스트로 변환
print(train_sents)

train_x = [sent2features(sent) for sent in train_sents] #[형태소,태그] 리스트를 가지고 형태소간의 index 정보를 추가한 리스트로 변환
print(train_x)
train_y = [sent2tags(sent) for sent in train_sents] #[형태소, 태그] 리스트를 가지고 tag정보들 반환
print(train_y)

trainer = pycrfsuite.Trainer() #학습객체 생성
for x, y in zip(train_x, train_y):
    trainer.append(x, y) #해당 형태소의 앞뒤의 형태소정보와 태그 정보를 가지고 학습
trainer.train('model.crfsuite')


tagger = pycrfsuite.Tagger()
tagger.open('model.crfsuite')

true_list = [] #정답을 저장할 리스트
test_sents = inputToList('train.txt',true_list) #train.txt를 읽어서 [형태소,태그]들의 리스트로 변환
test_x = [sent2features(sent) for sent in test_sents] #[형태소,태그] 리스트를 가지고 형태소간의 index 정보를 추가한 리스트로 변환
test_y = [sent2tags(sent) for sent in test_sents] #[형태소, 태그] 리스트를 가지고 tag정보들 반환

pred_y = [tagger.tag(x) for x in test_x] #예측값 도출
print(pred_y)

test_result(true_list,pred_y) #정답과 예측값을 비교하는함수