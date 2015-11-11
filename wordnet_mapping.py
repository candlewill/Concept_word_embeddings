__author__ = 'NLP-PC'
from nltk.corpus import wordnet as wn

from save_data import save_csv
from load_data import load_anew
from load_data import load_extend_anew
from load_data import load_csv


# returning the synsets of one word
def get_synsets(word):
    result = set()
    result.add(word)
    synsets = wn.synsets(word)
    for synset in synsets:
        result.add(str(synset.name()).split('.')[0])
    result.remove(word)
    return [word] + sorted(list(result))


# calculate synsets of words from a dictonary, eg. ANEW or others
def build_synsets(vocabulary):
    save_csv([get_synsets(v) for v in vocabulary], './data/synsets/extend_ANEW_synsets.csv')


def generate_anew_synsets_data():
    anew_words,_,_ = load_anew('./resource/ANEW.txt')
    build_synsets(anew_words)
    print('Saved.')
    print(anew_words)

def generate_extend_anew_synsets_data():
    anew_words,_,_ = load_extend_anew()
    build_synsets(anew_words)
    print('Saved.')


def replacer(word=None):
    syn_map = dict()
    synsets = load_csv('./data/synsets/ANEW_synsets.csv')
    for synset in synsets:
        if len(synset)>1:
            for w in synset[1:]:
                syn_map[w]=synset[0]

    # if word in syn_map.keys():
    #     return syn_map[word]
    return syn_map

if __name__ == "__main__":
    print(replacer('well'))
    exit()
    v=['bag', 'good', 'bad', 'cyand']
    build_synsets(v)
    exit()
    print(get_synsets('bag'))
    print(get_synsets('good'))
    print(get_synsets('bad'))


    # def map_word2synset(word)
