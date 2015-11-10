# Concept Level Word Embeddings
# 概念级别的词向量


本程序目标是训练概念级别的句向量，以分析替换情感词为其对应的概念后是否对构造句向量有影响。具体而言，本程序提供如下功能：

- 提供一个用于训练原始词向量的语料库
- 我们将上述语料库中的词汇，属于ANEW词典中的那部分情感词，按照WordNet同义词典进行替换，得到另一个概念语料库
- 我们用上述两个语料库，使用Doc2vec工具训练两份句项量
- 我们对这两份句向量，对于其中有VA标记的部分，使用简单的线性回归技术，分析他们在预测VA时性能表现是否有差距

### 动机

进行本实验的动机是，我们观察到无论是使用Word2vec训练词向量，还是使用Doc2vec训练句向量，都面临一个问题，训练出的向量更多的表达的是语义相似性而非情感相似性，如，good和bad虽然表达的是相反的情感倾向，但由于其出现的上下文较相似，因此这两个词向量的比较相似。为了解决这个问题，我们提出对语料库进行特殊的预处理，将语料库中的情感词替换为其对应的高层概念——synset编号。例如，在WordNet同义词典中，baby和child属于同义词，因此对于语料库中出现baby和child的地方我们用synset_id替换。

### Synset替换需要克服的问题

由于在wordnet中，仅仅使用同义词数量较少，如果使用同义词和lemma_names则Synset之间交叉多，如何解决这一问题？我们目前仅仅使用同义词进行替换，而不使用lemma_names，一方面是因为这样会导致Synset数量尽量多，另一方面实现起来较容易。

另一个问题，如何划分词汇到不同的Synset，注意只考虑替换给定词典(如ANEW)中词汇。Map words to synset id, 步骤如下：

* 计算所有ANEW中词汇的Synset
* 替换：对于一组相似同义词，用其中出现在ANEW词典中的词来替换掉语料库中其他所有词，例如，flag一词依据wordnet其同义词有：ease_up, iris, masthead, pin, sag，因此我们将语料库中所有ease_up, iris, masthead, pin, sag词汇用flag一次替换。注意：由于wordnet返回的词语中，包含了短语，如ease_up，用下划线连接起来的，对于这种情况，我们暂不处理。
* 速度优化：数据结构使用dict()

### 语料库

因为使用Doc2vec来训练句向量是非监督式的，但是为了判断句向量质量，我们使用监督式方式，因此语料库分为两类：unlabeled data和labeled data

* Unlabeled data: Stanford twitter corpus from sentiment140
* Labeled data: Vader Twitter corpus

### 句向量质量评估

对于用替换和不替换的语料库训练的两份句向量，我们使用其中的labeled data部分，训练一个回归模型，通过分析回归模型的性能，来判断句向量的质量。

### 版本

0.1.1

