__author__ = 'NLP-PC'
# coding: utf-8
import csv
import os
import pickle
import gensim
from gensim.models import Doc2Vec


def load_anew(filepath=None):
    with open(filepath, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        words, arousal, valence = [], [], []
        for line in reader:
            words.append(line[0])
            valence.append(float(line[1]))
            arousal.append(float(line[2]))
    return words, valence, arousal


def load_extend_anew(D=False):
    print('Loading extend_anew lexicon')
    with open('./resource/extend_ANEW.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        words, arousal, valence, dominance = [], [], [], []
        for line in reader:
            if reader.line_num == 1:
                continue
            words.append(line[1])
            arousal.append(float(line[5]))
            valence.append(float(line[2]))
            if D == True:
                dominance.append(float(line[8]))
    print('Loading extend_anew lexicon complete')
    if D == True:
        return words, valence, arousal, dominance
    else:
        return words, valence, arousal


def load_csv(filename):
    out = []
    with open(filename, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f, quoting=csv.QUOTE_NONE)
        for line in reader:
            out.append(line)
    return out

def load_sentiment140(filename):
    print('start loading data...')
    # ��ʽ��"4","1467822272","Mon Apr 06 22:22:45 PDT 2009","NO_QUERY","ersle","I LOVE @Health4UandPets u guys r the best!! "
    with open(filename, 'rt', encoding='ISO-8859-1') as f:
        inpTweets = csv.reader(f, delimiter=',', quotechar='"')
        X = []  # sentiment
        Y = []  # tweets
        for row in inpTweets:
            sentiment = (1 if row[0] == '4' else 0)
            tweet = row[5]
            X.append(sentiment)
            Y.append(tweet)
        # end loop
        return Y, X

def load_vader(filename):
    with open(filename, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        texts, ratings = [], []
        for line in reader:
            texts.append(line[2])
            ratings.append(float(line[1]))
    return texts, ratings


def load_embeddings(arg=None):
    if arg == 'zh_tw':  # dim = 400
        model = gensim.models.Word2Vec.load_word2vec_format(None, binary=False)
    elif arg == 'CVAT':  # dim = 50
        model = gensim.models.Word2Vec.load(None)
    elif arg == 'twitter':  # dim = 50
        model = Doc2Vec.load('./data/acc/docvecs_twitter.d2v')
    else:
        raise Exception('Wrong Argument.')
    print('Load Model Complete.')
    return model


def load_pickle(filename):
    out = pickle.load(open(filename, "rb"))
    return out
