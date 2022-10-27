import jieba
import jieba.analyse

#得到所有的特征词allwords
def wordget(danmu,stopwords,allwords):
    wordcutlist=wordcut(danmu,stopwords)
    for word in wordcutlist:
        if word in allwords.keys():
            allwords[word]+=1
        if word not in allwords.keys():
            allwords[word]=1
    return 0

def wordget1(danmu,stopwords,allwords):
    wordcutlist=wordcut(danmu,stopwords)
    for word in wordcutlist:
        count=wordcutlist.get(word,0)
        wordcutlist[word]=count+1

#返回该条弹幕对应的分词结果wordcutlist
def wordcut(danmu,stopwords):
    pre_wordcutlist = jieba.lcut(danmu)
    wordcutlist = []
    for preword in pre_wordcutlist:
        if preword not in stopwords and preword!=' ':
            wordcutlist.append(preword)
    return wordcutlist