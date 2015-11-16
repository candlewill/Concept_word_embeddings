from load_data import load_csv


def merge_synonym():
    synsets = load_csv('./data/synsets/ANEW_synsets.csv')
    syn_clusters = []
    for i, synset_i in enumerate(synsets):
        for synset_j in synsets[i + 1:]:
            if synset_i[0] in synset_j or synset_j[0] in synset_i:
                syn_cluster = (synset_i[0], synset_j[0])
                syn_clusters.append(syn_cluster)
    # zz = set()
    # for ll in syn_clusters:
    #     zz=zz.union(set(ll))
    # print(len(zz))
    # exit()
    tmp = syn_clusters
    outs = []
    for a, b in tmp:
        # 如果a, b 都没有出现过
        if all(len(set([a, b]) & set(l)) == 0 for l in outs):
            # 创建新的
            out = [a, b]
            outs.append(out)
        # 否则
        else:
            # 合并进去
            for i, l in enumerate(outs):
                if set([a, b]) & set(l) != set():
                    outs[i] = list(set(outs[i] + [a, b]))
                    break
    leng = 0
    for i, j in enumerate(outs):
        leng += len(j)
        print('| cluster_%s | %s |' % (str(i), str(j)))
    print(leng)

if __name__ == '__main__':
    merge_synonym()
