__author__ = 'NLP-PC'
import numpy as np
import random
import re
import string
from load_data import load_pickle
from gensim.models.word2vec import Word2Vec
from gensim import utils
from gensim.models.doc2vec import TaggedDocument
from gensim.models import Doc2Vec
from load_data import load_vader
from load_data import load_sentiment140
from save_data import dump_picle


class TaggedLineSentence(object):
    def __init__(self, labeled_data, unlabeled_data):
        self.data = labeled_data + unlabeled_data
        self.L_len = len(labeled_data)
        self.tagged_sentences = []

    def __iter__(self):
        for (id, sentence) in enumerate(self.data):
            if id < self.L_len:
                yield TaggedDocument(sentence.split(' '), tags=['L_SENT_%s' % str(id)])
            else:
                yield TaggedDocument(sentence.split(' '), tags=['U_SENT_%s' % str(id)])

    def to_array(self):
        for (id, sentence) in enumerate(self.data):
            if id < self.L_len:
                self.tagged_sentences.append(
                    TaggedDocument(words=sentence.split(' '), tags=['L_SENT_%s' % str(id)]))
            else:
                self.tagged_sentences.append(
                    TaggedDocument(words=sentence.split(' '), tags=['U_SENT_%s' % str(id)]))
        return self.tagged_sentences

    def sentences_rand(self):
        random.shuffle(self.tagged_sentences)
        return self.tagged_sentences


def train_docvecs(Sentences):
    model = Doc2Vec(min_count=10, window=8, size=300, sample=1e-5, negative=5, workers=4)
    model.build_vocab(Sentences.to_array())
    for epoch in range(100):
        print('epoch: %s' % epoch)
        model.train(Sentences.sentences_rand())
    model.save('./data/acc/docvecs_twitter.d2v')
    print('Training model complete, saved successful.')


def preprocess(texts, replace=False):
    # 表情符号替换，只采用那些明显带有正面或者负面情感的词语来替代
    emo_repl = {
        # 正面情感的表情
        '&lt;3': 'good',
        ':d': 'good',
        ':dd': 'good',
        '8)': 'good',
        ':-)': 'good',
        ':)': 'good',
        ';)': 'good',
        '(-:': 'good',
        '(:': 'good',

        # 负面情感的表情
        ':/': 'bad',
        ':&gt;': 'sad',
        ":')": 'sad',
        ":-(": 'bad',
        ':(': 'bad',
        ':S': 'bad',
        ':-S': 'bad',

        # neural html taggers
        '&amp;': 'and',
    }
    # 确保:DD在:D之前替换，即先替换:DD，后替换:D
    emo_repl_order = [k for (k_len, k) in reversed(sorted([(len(k), k) for k in emo_repl.keys()]))]

    # 利用正则表达式及其扩展（\b标记出词语边界）来定义那些缩写形式
    re_repl = {
        # 缩写替换
        r"\br\b": "are",  # r -> are
        r"\bu\b": "you",  # u -> you
        r"\bhaha\b": "ha",  # haha -> ha
        r"\bhahaha\b": "ha",  # hahaha -> ha
        r"\bdon't\b": "do not",  # don't -> do not
        r"\bdoesn't\b": "does not",  # dosen't -> does not
        r"\bdidn't\b": "did not",  # didn't -> did not
        r"\bhasn't\b": "has not",  # hasn't -> has not
        r"\bhaven't\b": "have not",  # haven't -> have not
        r"\bhadn't\b": "had not",  # hadn't -> had not
        r"\bwon't\b": "will not",  # won't -> will not
        r"\bwouldn't\b": "would not",  # woudn't  -> would not
        r"\bcan't\b": "can not",  # can't -> can not
        r"\bcannot\b": "can not",  # cannot -> can not
        r"\bthey're\b": "they are",  # they're -> they are
        r"\bit's\b": "it is",  # it's -> it is
        r"\byou're\b": "you are",  # you're -> you are
        r"\bit'll\b": "it will",  # it's -> it will
        r"\bi'm\b": "i am",  # i'm -> i am
        r"\bwe'll\b": "we will",  # we'll -> we will
        r"\bwe're\b": "we are",  # we're -> we are
        r"\bwhat's\b": "what is",  # what's -> what is
        r"\bshe's\b": "she is",  # she's -> she is
        r"\bisn't\b": "is not",  # isn't -> is not
        r"\bcouldn't\b": "could not",  # couldn't -> could not
        r"\bthat's\b": "that is",  # that's -> that is
        r"\bhe's\b": "he is",  # he's -> he is
        r"\bthere's\b": "there is",  # there's -> there is
        r"\bwe've\b": "we have",  # we've -> we have
        r"\byou'll\b": "you will",  # you'll -> you will
        r"\bi'll\b": "i will",  # i'll -> i will
        r"\bi've\b": "i have",  # i've -> i have
        r"\bshouldn't\b": "should not",  # shouldn't -> should not
        r"\bwasn't\b": "was not",  # wasn't -> was not
        r"\bi'd\b": "i would",  # i'd -> i would
        r"\blet's\b": "let us",  # let's -> let us
        r"\byou'd\b": "you would",  # you'd -> you would
        r"\byou've\b": "you have",  # you've -> you have
        r"\bwho's\b": "who is",  # who's -> who is
        r"\bshe'll\b": "she will",  # she'll -> she will
        r"\baren't\b": "are not",  # aren't -> are not

        # 利用正则表达式，替换其他
        r'((www\.[^\s]+)|(https?://[^\s]+))': 'url',  # www.baidu.com or http: -> url
        r'@[^\s]+': 'someone',  # @someone -> someone
        r'#([^\s]+)': r'\1',  # # topic -> topic
        r"(.)\1{1,}": r"\1\1",  # noooooope -> noope
        # r" +": " ", # 删去多余空格
        r"\bhttp[^\s]+\b": 'url',  # 以http开始的单词 ->url
    }

    def isEnglish(s):
        try:
            s.encode('ascii')
        except UnicodeEncodeError:
            return False
        else:
            return True

    preprocessed = []
    for tweet in texts:
        # if isEnglish(tweet):
        tweet = tweet.lower()
        for k in emo_repl_order:
            tweet = tweet.replace(k, emo_repl[k])

        for r, repl in re_repl.items():
            tweet = re.sub(r, repl, tweet)

        # remove all punctuation
        for c in string.punctuation:
            tweet = tweet.replace(c, " ")
        tweet = re.sub(r" +", " ", tweet).strip()  # 删除单词之间的多余空格
        preprocessed.append(tweet.strip())
    return preprocessed


# Train doc2vec
def train_doc2vec():
    # def isEnglish(s):
    #     try:
    #         s.encode('ascii')
    #     except UnicodeEncodeError:
    #         return False
    #     else:
    #         return True

    labeled_data, _ = load_vader('./resource/tweets.txt')
    # for i,d in enumerate(labeled_data):
    #     print(i)
    #     if not isEnglish(d):
    #         print('*'*111)
    #         print(i,d)
    # exit()
    unlabeled_data, _ = load_sentiment140('/home/hs/Data/Corpus/training.csv')
    labeled_data = preprocess(labeled_data, replace=False)
    dump_picle(labeled_data, './data/acc/labeled_data.p')
    unlabeled_data = preprocess(unlabeled_data, replace=False)
    dump_picle(unlabeled_data, './data/acc/unlabeled_data.p')
    # labeled_data = load_pickle('./data/acc/labeled_data.p')
    # unlabeled_data = load_pickle('./data/acc/unlabeled_data.p')
    sentence = TaggedLineSentence(labeled_data, unlabeled_data)
    train_docvecs(sentence)


if __name__ == "__main__":
    train_doc2vec()
