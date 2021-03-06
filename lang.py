import jieba
import jieba.posseg
import jieba.analyse
import json
import help
import synonyms
import parameter

def segWord(sen,nwfound=True):
    gen=jieba.cut(sen,HMM=nwfound)
    list=[]
    for i in gen:
        list.append(i)
    return list

def loadDict(path):
    jieba.load_userdict(path)

def addWord(word,freq,tag):
    jieba.add_word(word,freq=freq,tag=tag)

def easyAddWord(word): #也可传递希望强制分割的连续列表
    jieba.suggest_freq(word,True)

def POStag(sen,nwfound=True):
    gen=jieba.posseg.cut(sen,HMM=nwfound)
    list = []
    for i in gen:
        list.append([i.word,i.flag])
    return list

def summary(sen,topK=5,withWeight=False):
    return jieba.analyse.textrank(sen, topK = topK, withWeight = withWeight)

def isStopWord(word):
    nowhead=help.gethead(word)
    for k in stoplist.keys():
        if k==nowhead:
            for i in stoplist[k]:
                if i==word:
                    return True
            return False #循环完了都没有

def init(swpath,spath):
    jsoncode=help.readTXT(swpath)
    global stoplist
    stoplist=json.loads(jsoncode)
    synonyms.init(spath)

def isSynonyms(word1,word2):
    return synonyms.isSynonyms(word1,word2)

def getSim(sen1,sen2,minlen=5,topK=5): # 接受list形式的sen
    if len(sen1)<=minlen or len(sen2)<=minlen:
        return -1
    sen1=help.listToStr(sen1)
    sen2 = help.listToStr(sen2)
    s1sum=set(summary(sen1,topK=topK))
    s2sum=set(summary(sen2,topK=topK))
    if len(s1sum)==0 or len(s2sum)==0:
        return -1
    else:
        return len(s1sum&s2sum)/len(s1sum|s2sum)

def isSim(sen1,sen2,minlen=5,topK=5):
    return getSim(sen1,sen2,minlen,topK)>=parameter.simThreshold

def equBayes(char,word):
    result=word*2/char
    return help.limitDigits(result)

def isRepeat(sen):
    for w in sen:
        if isStopWord(w):
            continue
        if help.caluCount(sen,w)>parameter.repeatLimit:
            return True
    return False