from __future__ import unicode_literals, print_function

import re
import codecs
import pycrfsuite
from itertools import chain
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelBinarizer

def raw2corpus(raw_path, corpus_path):
    raw = codecs.open(raw_path, encoding='utf-8')
    raw_sentences = raw.read().split('\n')
    corpus = codecs.open(corpus_path, 'w', encoding='utf-8')
    sentences = []
    for raw_sentence in raw_sentences:
        if not raw_sentence:
            continue
        text = re.sub(r'(\ )+', ' ', raw_sentence).strip()
        taggeds = []
        for i in range(len(text)):
            if i == 0:
                taggeds.append('{}/B'.format(text[i]))
            elif text[i] != ' ':
                successor = text[i - 1]
                if successor == ' ':
                    taggeds.append('{}/B'.format(text[i]))
                else:
                    taggeds.append('{}/I'.format(text[i]))
        sentences.append(' '.join(taggeds))
    corpus.write('\n'.join(sentences))

def corpus2raw(corpus_path, raw_path):
    corpus = codecs.open(corpus_path, encoding='utf-8')
    corpus_sentences = corpus.read().split('\n')
    raw = codecs.open(raw_path, 'w', encoding='utf-8')
    sentences = []
    for corpus_sentence in corpus_sentences:
        taggeds = corpus_sentence.split(' ')
        text = ''
        len_taggeds = len(taggeds)
        for tagged in taggeds:
            try:
                word, tag = tagged.split('/')
                if word and tag:
                    if tag == 'B':
                        text += ' ' + word
                    else:
                        text += word
            except:
                pass
        sentences.append(text.strip())
    raw.write('\n'.join(sentences))

def corpus2sent(path):
    corpus = codecs.open(path, encoding='utf-8').read()
    raws = corpus.split('\n')
    sentences = []
    for raw in raws:
        tokens = raw.split(' ')
        sentence = []
        for token in tokens:
            try:
                word, tag = token.split('/')
                if word and tag:
                    sentence.append([word, tag])
            except:
                pass
        sentences.append(sentence)
    return sentences

def index2feature(sent, i, offset):
    word, tag = sent[i + offset]
    if offset < 0:
        sign = ''
    else:
        sign = '+'
    return '{}{}:word={}'.format(sign, offset, word)

#좌우 7글자까지를 보면서 해당 인덱스의 글자에 태그를 맞추는 조건부 확률 문제로 생각
def word2features(sent, i):
    L = len(sent)
    word, tag = sent[i]
    features = ['bias']
    features.append(index2feature(sent, i, 0))

    if i > 6:
        features.append(index2feature(sent, i, -7))
    if i > 5:
        features.append(index2feature(sent, i, -6))
    if i > 4:
        features.append(index2feature(sent, i, -5))
    if i > 3:
        features.append(index2feature(sent, i, -4))
    if i > 2:
        features.append(index2feature(sent,i,-3))
    if i > 1:
        features.append(index2feature(sent, i, -2))
    if i > 0:
        features.append(index2feature(sent, i, -1))
    else:
        features.append('bos')

    if i < L - 7:
        features.append(index2feature(sent, i, 7))
    if i < L - 6:
        features.append(index2feature(sent, i, 6))
    if i < L - 5:
        features.append(index2feature(sent,i,5))
    if i < L - 4:
        features.append(index2feature(sent,i,4))
    if i < L - 3:
        features.append(index2feature(sent,i,3))
    if i < L - 2:
        features.append(index2feature(sent, i, 2))
    if i < L - 1:
        features.append(index2feature(sent, i, 1))
    else:
        features.append('eos')
    return features

def sent2words(sent):
    return [word for word, tag in sent]

def sent2tags(sent):
    return [tag for word, tag in sent]

def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]

def report(test_y, pred_y):
    lb = LabelBinarizer()
    test_y_combined = lb.fit_transform(list(chain.from_iterable(test_y)))
    pred_y_combined = lb.transform(list(chain.from_iterable(pred_y)))
    tagset = sorted(set(lb.classes_))
    class_indices = {cls: idx for idx, cls in enumerate(tagset)}
    print(classification_report(test_y_combined, pred_y_combined, labels=[class_indices[cls] for cls in tagset], target_names=tagset))

def inputToList(f_name):
    input_f = open(f_name, 'r', encoding='utf-8')
    sentences = []
    sentence = []
    for line in input_f:
        try :
            word,tag = line.split(' ')

            word = word.replace(u'\ufeff', '')
            if word == 'φ':
                sentences.append(sentence)
                sentence = []
                continue
        except:
            pass
        sentence.append([word, tag.rstrip()])
    return sentences


train_sents = inputToList('train.txt')
test_sents = inputToList('test.txt')
train_x = [sent2features(sent) for sent in train_sents]
train_y = [sent2tags(sent) for sent in train_sents]
test_x = [sent2features(sent) for sent in test_sents]
test_y = [sent2tags(sent) for sent in test_sents]


trainer = pycrfsuite.Trainer()
for x, y in zip(train_x, train_y):
    trainer.append(x, y)
trainer.train('model.crfsuite')


tagger = pycrfsuite.Tagger()
tagger.open('model.crfsuite')

pred_y = [tagger.tag(x) for x in test_x]

def flush(path, X, Y):
    result = codecs.open(path, 'w', encoding='utf-8')
    for x, y in zip(X, Y):
        result.write(' '.join(['{}/{}'.format(feature[1].split('=')[1], tag) for feature, tag in zip(x, y)]))
        result.write('\n')
    result.close()

flush('prediction.txt', test_x, pred_y)
corpus2raw('prediction.txt', 'line_predict.txt')

report(test_y, pred_y)
