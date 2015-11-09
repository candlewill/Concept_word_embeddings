__author__ = 'NLP-PC'
import numpy as np
import random

from gensim.models.word2vec import Word2Vec
from gensim import utils
from gensim.models.doc2vec import TaggedDocument
from gensim.models import Doc2Vec

from load_data import load_vader
from load_data import load_sentiment140

class TaggedLineSentence(object):
    def __init__(self, labeled_data, unlabeled_data):
        self.labeled_data = labeled_data
        self.unlabeled_data = unlabeled_data
        self.tagged_sentences = []

    def __iter__(self):
        for (id, sentence) in enumerate(self.labeled_data):
            yield TaggedDocument(sentence, tags=['L_SENT_%s' % str(id)])
        for (id, sentence) in enumerate(self.unlabeled_data):
            yield TaggedDocument(sentence, tags=['U_SENT_%s' % str(id)])

    def to_array(self):
        for (id, sentence) in enumerate(self.labeled_data):
            self.tagged_sentences.append(
                TaggedDocument(words=sentence, tags=['L_SENT_%s' % str(id)]))
        for (id, sentence) in enumerate(self.unlabeled_data):
            self.tagged_sentences.append(
                TaggedDocument(words=sentence, tags=['U_SENT_%s' % str(id)]))

        return self.tagged_sentences

    def sentences_rand(self):
        random.shuffle(self.tagged_sentences)
        return self.tagged_sentences


def train_docvecs(Sentences):
    model = Doc2Vec(min_count=2, window=10, size=50, sample=1e-5, negative=5, workers=7)
    model.build_vocab(Sentences.to_array())
    for epoch in range(10):
        print('epoch: %s' % epoch)
        model.train(Sentences.sentences_rand())
    model.save('./data/acc/docvecs_twitter.d2v')
    print('Training model complete, saved successful.')

# Train doc2vec
def train_doc2vec():
    labeled_data, _ = load_vader('./resource/tweets.txt')
    unlabeled_data, _ = load_sentiment140('./resource/test_data.txt')
    sentence = TaggedLineSentence(labeled_data, unlabeled_data)
    train_docvecs(sentence)

if __name__ == "__main__":
    train_doc2vec()