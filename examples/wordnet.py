__author__ = 'NLP-PC'
# all examples about wordnet from http://www.nltk.org/howto/wordnet.html
from nltk.corpus import wordnet as wn
game = wn.synsets('color')
for n in game:
    print(n.name())

exit()
print(game[-1].similar_tos())

print()

for ss in wn.synsets('game'):
    print(ss.name(), ss.lemma_names())
exit()

for synset in list(wn.all_synsets('n'))[:10]:
    print(synset)


print(wn.synsets('dog', pos=wn.VERB))
print("*"*111)
print(wn.synset('dog.n.01'))
print(wn.synset('dog.n.01').definition())
print(len(wn.synset('dog.n.01').examples()))
print(wn.synset('dog.n.01').examples()[0])
print(wn.synset('dog.n.01').lemmas())
a = [str(lemma.name()) for lemma in wn.synset('dog.n.01').lemmas()]
print(a)
print(wn.lemma('dog.n.01.dog').synset())
print("*"*111)
print(sorted(wn.langs()))
print(wn.synsets(b'\xe7\x8a\xac'.decode('utf-8'), lang='jpn'))
print(wn.synset('spy.n.01').lemma_names('jpn'))
print(wn.synset('dog.n.01').lemma_names('ita'))
print("*"*111)

dog = wn.synset('dog.n.01')
print(dog.hypernyms())
print(dog.hyponyms())
print(dog.member_holonyms())
print(dog.root_hypernyms())
print(wn.synset('dog.n.01').lowest_common_hypernyms(wn.synset('cat.n.01')))
print("*"*111)

good = wn.synset('good.a.01')
# print(good.antonyms())
print(good.lemmas()[0].antonyms())
print("*"*111)

dog = wn.synset('dog.n.01')
cat = wn.synset('cat.n.01')
hit = wn.synset('hit.v.01')
slap = wn.synset('slap.v.01')

print("*"*111)
#Walk through the noun synsets looking at their hypernyms:
from itertools import islice
for synset in islice(wn.all_synsets('n'), 5):
    print(synset, synset.hypernyms())