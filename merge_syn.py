from load_data import load_csv


def merge_synonym():
    synsets = load_csv('./data/synsets/ANEW_synsets.csv')
    for i, synset_i in enumerate(synsets):
        for j, synset_j in enumerate(synsets[i + 1:]):
            if synset_i[0] in synset_j and synset_j[0] in synset_i:
                print(synset_i[0], synset_j[0])


if __name__ == '__main__':
    merge_synonym()
