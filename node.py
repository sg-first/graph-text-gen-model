import lang
import parameter

class node:
    word = ""
    behindStop = None  # [stopWord],句尾停用词
    frontStop = None  # 句首停用词
    behindNode = None  # [{node,P,isPass,[stopWord]}]，后向接边
    frontNode = None  # 前向接边
    synonymNode = None # [{node,isPass}]，同义边
    activation = 0
    firstp = 0  # 该词出现在句首的概率
    caluForm = None # [{c:v}]
    wordCount = 0 # 在训练集中出现次数

    def changeNode(self, anode, delta, nodelist):  # Private
        for nunion in nodelist:
            if nunion["node"].word == anode.word:
                nunion["P"] += delta
                return nunion
        # 没有，添加
        newelm={"node":anode,"P":delta,"isPass":False,"stopList":[]}
        nodelist.append(newelm)
        return newelm

    def addStopWord(self,elmlist,word,delta):  # Private
        for i in elmlist:
            if i.word==word:
                i.p+=delta
                return
        # 没有，添加
        newStopWord=stopWord(word,delta)
        elmlist.append(newStopWord)

    def autoChangeBehindNode(self,node1,node2,word1,delta):
        if not node1 is None:
            self.changeNode(node1, delta, self.behindNode)
            return
        else:
            if node2 is None:  # 上层要至少保证word1不是None（不越界）
                self.addStopWord(self.behindStop, word1, delta)  # word1为尾词停止，调整behindStop
                return
            else:
                elm = self.changeNode(node2, delta, self.behindNode)
                self.addStopWord(elm["stopList"], word1, delta)
                return

    def autoChangeFrontNode(self,node1,node2,word1,delta):
        if not node1 is None:
            self.changeNode(node1, delta, self.frontNode)
            return
        else:
            if node2 is None:  # 上层要至少保证word1不是None（指越界）
                self.addStopWord(self.frontStop, word1, delta)  # word1为首词停止，调整frontStop
                return
            else:
                elm = self.changeNode(node2,delta,self.frontNode)
                self.addStopWord(elm["stopList"], word1, delta)
                return

    def addSynonyms(self,n):
        for spair in self.synonymNode:
            if spair["node"].word==n.word: #正面有，反面就有，反之亦然
                return
        self.synonymNode.append({"node": n, "isPass": False})
        n.synonymNode.append({"node": self, "isPass": False})

    def __init__(self, word):
        self.word = word
        self.behindStop = []
        self.frontStop = []
        self.behindNode = []
        self.frontNode = []
        self.synonymNode = []
        self.caluForm = []

class stopWord:
    word = ""
    p = 0

    def __init__(self,word,delta):
        self.word=word
        self.p=delta

def genStopWord(elmlist):
    maxp=parameter.minstop
    maxstop=None
    for i in elmlist:
        if i.p>maxp:
            maxp=i.p
            maxstop=i.word
    return maxstop

def wordFindNode(wordmap,word):
    for n in wordmap:
        if n.word==word:
            return n
    return None

def findornew(wordmap,word):
    nw1 = wordFindNode(wordmap, word)
    if nw1 is None:
        nw1 = node(word)
        wordmap.append(nw1)
    return nw1

def wordFindNodeList(wordmap,wordList): #批量转换
    result=[]
    for n in wordmap:
        for c in range(len(wordList)): #每个词都遍历一遍
            if n.word==wordList[c]:
                result.append(n)
                del wordList[c]
                break
    return result

def getLastForm(list):
    return list[len(list) - 1]