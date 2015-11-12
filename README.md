# Concept Level Word Embeddings
# 概念级别的词向量


本程序目标是训练概念级别的句向量，以分析替换情感词为其对应的概念后是否对构造句向量有影响。具体而言，本程序提供如下功能：

- 提供一个用于训练原始词向量的语料库
- 我们将上述语料库中的词汇，属于ANEW词典中的那部分情感词，按照WordNet同义词典进行替换，得到另一个概念语料库
- 我们用上述两个语料库，使用Doc2vec工具训练两份句项量
- 我们对这两份句向量，对于其中有VA标记的部分，使用简单的线性回归技术，分析他们在预测VA时性能表现是否有差距

### 动机

进行本实验的动机是，我们观察到无论是使用Word2vec训练词向量，还是使用Doc2vec训练句向量，都面临一个问题，训练出的向量更多的表达的是语义相似性而非情感相似性，如，good和bad虽然表达的是相反的情感倾向，但由于其出现的上下文较相似，因此这两个词向量的比较相似。

### 方法

为了解决这个问题，我们提出对语料库进行特殊的预处理，将语料库中的情感词替换为其对应的高层概念——synset编号。例如，在WordNet同义词典中，baby和child属于同义词，因此对于语料库中出现baby和child的地方我们用synset_id替换。
在NLTK提供的wordnet工具中，提供了每一个词汇的同义词，然而并没有synset ID。因此，我们将ANEW中同义词替换为ANEW中的词汇。也就是说，我们通过wordnet搜寻所有ANEW中词汇的同义词，然后出现同义词的地方用anew替换。例如：
替换之前的文本如下图：

![替换之前](http://7xo9ej.com1.z0.glb.clouddn.com/替换之后.png "图1：替换之前")

替换之后的文本如下图：

![替换之后](http://7xo9ej.com1.z0.glb.clouddn.com/替换之前.png "图2：替换之后")

从上图中可以发现，第一行中，love替换为了passion，第二行中good替换为了serious。这是因为passion和serious为ANEW词典中的词汇，而依据wordnet，love是passion的同义词，good是serious的同义词，见wordnet[在线演示网址](http://wordnetweb.princeton.edu/perl/webwn?s=serious&sub=Search+WordNet&o2=&o0=1&o8=1&o1=1&o7=&o5=&o9=&o6=&o3=&o4=&h=0000000)，其他替换方式类同。更多详细比较，见resource目录中的相关txt文件。


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

### 对比

我们分别训练了这几种句向量：

* 不做任何预处理
* 有预处理，预处理之后的语料库存储为pickle格式，方便下次直接加载
* 有预处理，并且进行同义词替换，同样处理后的结构用pickle存储

### Setup

* 词向量维数：300
* windows size: 8
* min count: 10
* epoch: 100

### 实验结果

概括：有预处理比没有预处理性能好，同义词是否替换对实验结果影响不大

#### 比较结果

没有预处理：

| Metrics        | MSE           | MAE  |Pearson_r|
| ------------- |-------------| ------------| ------------- |
| ordinary least squares      | 1.49259610132 | 0.970785105026 | 0.61255020512241898 |
| Ridge Regression     | 1.484225097| 0.967602444956 | 0.61426306602239911 |
| Bayesian Regression      | 1.45401467863 | 0.954559329101 | **0.62166130478403103** |
| SVR      | 1.546847209 | 0.980544878277 | 0.59874022849588793 |
| KNN Reg      | 2.27236965663 | 1.15422092554 | 0.39873708455401208 |

有预处理：

| Metrics        | MSE           | MAE  |Pearson_r|
| ------------- |-------------| ------------| ------------- |
| ordinary least squares      | 1.18588698657| 0.861801766775 | 0.70756349588614698 |
| Ridge Regression              | 1.18039015402 | 0.860557769888 | 0.70886360511213908 |
| Bayesian Regression        |1.15727179209| 0.857067555413 | **0.71607752341210373** |
| SVR                                     | 1.20029817528 | 0.865424229004 | 0.70343288843448581|
| KNN Reg                            | 2.01645151621| 1.10575613528| 0.46131273504861253 |

预处理+同义词替换：

| Metrics        | MSE           | MAE  |Pearson_r|
| ------------- |-------------| ------------| ------------- |
| ordinary least squares      | 1.18038914619 | 0.85878648801 | 0.70974246423615184 |
| Ridge Regression              | 1.17572872216 |  0.857236881556 | 0.71066619047925106 |
| Bayesian Regression        |1.15633277046| 0.851493165039 | **0.71596164673843599**|
| SVR                                     | 1.20673631577| 0.866939930114| 0.70360523364732996 |
| KNN Reg                            | 2.14915481032 | 1.13988959412 | 0.44050915767949778|

#### 原始数据

没有预处理：
```
2015-11-11 21:43:32,627 - log_manager - INFO - linear regression Explained variance score: 0.37
2015-11-11 21:43:32,627 - log_manager - INFO - MSE: 1.49259610132, MAE: 0.970785105026, Pearson_r: (0.61255020512241898, 1.1548008591482935e-87), R2: -0.347502977953, Spearman_r: (0.60526409023253303, 4.3034245706995162e-85), sqrt_MSE: 1.2217185033067797
2015-11-11 21:43:32,672 - log_manager - INFO - linear regression Explained variance score: 0.37
2015-11-11 21:43:32,672 - log_manager - INFO - MSE: 1.484225097, MAE: 0.967602444956, Pearson_r: (0.61426306602239911, 2.8070099885082727e-88), R2: -0.376475902221, Spearman_r: (0.60719032867430034, 9.1309479255558613e-86), sqrt_MSE: 1.218287772656195
2015-11-11 21:43:32,989 - log_manager - INFO - linear regression Explained variance score: 0.39
2015-11-11 21:43:32,989 - log_manager - INFO - MSE: 1.45401467863, MAE: 0.954559329101, Pearson_r: (0.62166130478403103, 5.6384710397369307e-91), R2: -0.62660269397, Spearman_r: (0.6147146681658836, 1.9304616996028348e-88), sqrt_MSE: 1.2058253101633096
2015-11-11 21:43:41,873 - log_manager - INFO - linear regression Explained variance score: 0.35
2015-11-11 21:43:41,873 - log_manager - INFO - MSE: 1.546847209, MAE: 0.980544878277, Pearson_r: (0.59874022849588793, 7.5911317184794384e-83), R2: -0.353026259129, Spearman_r: (0.5963620872871338, 4.8577278002144607e-82), sqrt_MSE: 1.2437231239294992
2015-11-11 21:43:45,843 - log_manager - INFO - linear regression Explained variance score: 0.04
2015-11-11 21:43:45,844 - log_manager - INFO - MSE: 2.27236965663, MAE: 1.15422092554, Pearson_r: (0.39873708455401208, 2.1292244447399554e-33), R2: -0.937259773286, Spearman_r: (0.36715551558011367, 3.3360442239675783e-28), sqrt_MSE: 1.5074381103800916
```
有预处理：
```
2015-11-11 23:36:00,418 - log_manager - INFO - linear regression Explained variance score: 0.50
2015-11-11 23:36:00,418 - log_manager - INFO - MSE: 1.18588698657, MAE: 0.861801766775, Pearson_r: (0.70756349588614698, 1.6712736443956464e-128), R2: 0.084180966398, Spearman_r: (0.69406124970867411, 1.0008828505969173e-121), sqrt_MSE: 1.0889843830721149
2015-11-11 23:36:00,462 - log_manager - INFO - linear regression Explained variance score: 0.50
2015-11-11 23:36:00,462 - log_manager - INFO - MSE: 1.18039015402, MAE: 0.860557769888, Pearson_r: (0.70886360511213908, 3.5477223379727426e-129), R2: 0.0700383871262, Spearman_r: (0.69542180436110168, 2.1605994405743398e-122), sqrt_MSE: 1.0864576172228462
2015-11-11 23:36:00,808 - log_manager - INFO - linear regression Explained variance score: 0.51
2015-11-11 23:36:00,809 - log_manager - INFO - MSE: 1.15727179209, MAE: 0.857067555413, Pearson_r: (0.71607752341210373, 5.5770753916487455e-133), R2: -0.0465387422234, Spearman_r: (0.70315833348410628, 2.9948846691061593e-126), sqrt_MSE: 1.075765677128298
2015-11-11 23:36:10,740 - log_manager - INFO - linear regression Explained variance score: 0.49
2015-11-11 23:36:10,741 - log_manager - INFO - MSE: 1.20029817528, MAE: 0.865424229004, Pearson_r: (0.70343288843448581, 2.1734917238896289e-126), R2: 0.0637543322379, Spearman_r: (0.692565110336131, 5.3487916786057751e-121), sqrt_MSE: 1.0955812043299649
2015-11-11 23:36:14,885 - log_manager - INFO - linear regression Explained variance score: 0.15
2015-11-11 23:36:14,885 - log_manager - INFO - MSE: 2.01645151621, MAE: 1.10575613528, Pearson_r: (0.46131273504861253, 1.7051785857700428e-45), R2: -1.1185774545, Spearman_r: (0.40850869323860917, 4.0091512487600461e-35), sqrt_MSE: 1.420018139394025
```
预处理+同义词替换：
```
2015-11-12 13:37:10,299 - log_manager - INFO - linear regression Explained variance score: 0.50
2015-11-12 13:37:10,299 - log_manager - INFO - MSE: 1.18038914619, MAE: 0.85878648801, Pearson_r: (0.70974246423615184, 1.2383132100315053e-129), R2: 0.121271038151, Spearman_r: (0.70707766629922053, 2.9759233629594366e-128), sqrt_MSE: 1.0864571534069252
2015-11-12 13:37:10,388 - log_manager - INFO - linear regression Explained variance score: 0.50
2015-11-12 13:37:10,388 - log_manager - INFO - MSE: 1.17572872216, MAE: 0.857236881556, Pearson_r: (0.71066619047925106, 4.0787325544405145e-130), R2: 0.107070184954, Spearman_r: (0.70800020526544993, 9.9395544341388438e-129), sqrt_MSE: 1.0843102518001932
2015-11-12 13:37:10,710 - log_manager - INFO - linear regression Explained variance score: 0.51
2015-11-12 13:37:10,710 - log_manager - INFO - MSE: 1.15633277046, MAE: 0.851493165039, Pearson_r: (0.71596164673843599, 6.4333970885345271e-133), R2: -0.0188708366953, Spearman_r: (0.71316382374840792, 1.9808536854345207e-131), sqrt_MSE: 1.0753291451717815
2015-11-12 13:37:20,691 - log_manager - INFO - linear regression Explained variance score: 0.49
2015-11-12 13:37:20,691 - log_manager - INFO - MSE: 1.20673631577, MAE: 0.866939930114, Pearson_r: (0.70360523364732996, 1.7769804325105011e-126), R2: 0.135825053535, Spearman_r: (0.7029631109243577, 3.7607682055022545e-126), sqrt_MSE: 1.0985155054751432
2015-11-12 13:37:24,723 - log_manager - INFO - linear regression Explained variance score: 0.09
2015-11-12 13:37:24,723 - log_manager - INFO - MSE: 2.14915481032, MAE: 1.13988959412, Pearson_r: (0.44050915767949778, 3.4481452164542079e-41), R2: -1.25050146879, Spearman_r: (0.3756021409491484, 1.5459579149703661e-29), sqrt_MSE: 1.4659995942423818
```
### 版本

0.1.2

### License

[Yunchao He] @ [YZU]

### Contact Us

* yunchaohe@gmail.com
* [http://sentiment-mining.blogspot.com/]

**NOTICE: Still developing, more usefull function later.**

**Any advice and suggest would be welcomed, thank you.**

[Yunchao He]: https://facebook.com/yunchao.h
[http://sentiment-mining.blogspot.com/]: http://sentiment-mining.blogspot.tw/
[YZU]: http://www.yzu.edu.tw/