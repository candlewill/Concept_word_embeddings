from load_data import load_pickle


def analysis_preprocess():
    preprocessed = load_pickle('./data/acc/labeled_data.p')
    for id, i in enumerate(preprocessed):
        print('| %s | %s |' % (id, i))


if __name__ == '__main__':
    analysis_preprocess()
