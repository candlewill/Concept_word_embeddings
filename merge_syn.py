from load_data import load_csv
import copy


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
    outs = []
    for a, b in syn_clusters:
        # 如果a, b 都没有出现过
        if all(len(set([a, b]) & set(l)) == 0 for l in outs):
            # 创建新的
            out = [a, b]
            outs.append(out)
        # 否则
        else:
            # 合并进去
            for i, k in enumerate(outs):
                if set([a, b]) & set(k) != set():
                    outs[i] = list(set(outs[i] + [a, b]))
                    break

    # leng = 0
    # for i, j in enumerate(outs):
    #     leng += len(j)
    #     print('| cluster_%s | %s |' % (str(i), str(j)))
    # print(leng)
    return outs


def build_syn_map(ANEW_synsets, merged_ANEW):
    def find_index(word):
        for i, syn in enumerate(ANEW_synsets):
            if str(syn[0]) == str(word):
                return i
        print('__%s__' % word)

    outs = []
    for words in merged_ANEW:
        result = set()
        for w in words:
            ind = find_index(w)
            result = result | set(ANEW_synsets[ind])
            # print(result)
        outs.append(sorted(list(result)))

    for term in ANEW_synsets:
        if all(term[0] not in out for out in outs) and len(term) > 1:
            outs.append(term)
    # for iterm in outs:
    #     print('| %s | ``` %s ``` |' % (str(iterm[0]), str(iterm[1:])))
    # exit()
    syn_map = dict()
    for synset in outs:
        if len(synset) > 1:
            for m in synset[1:]:
                syn_map[m] = synset[0]

    # if word in syn_map.keys():
    #     return syn_map[word]
    return syn_map


def replacer():
    outs = merge_synonym()
    syn_map = load_csv('./data/synsets/ANEW_synsets.csv')
    replace_map = build_syn_map(syn_map, outs)
    print(replace_map['gusto'])
    return replace_map


if __name__ == '__main__':
    replacer()
