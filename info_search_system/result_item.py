from collections import defaultdict

import numpy as np


class ResultItem:
    def __init__(self,i_doc,doc_name,title,time,url,doc,score,words,terms):
        self.index = i_doc
        self.doc_name=doc_name
        self.title=title
        self.time=time
        self.url=url
        self.doc = doc
        self.score = score
        self.words=words
        self.freqs = np.zeros(len(words)) # 各个词出现的频率
        self.positions = defaultdict(list)
        self.terms=terms


    def __str__(self):
        s = "\ndoc_name: " + self.doc_name +\
            "\ntitle: " + self.title +\
            "\ntime: " + self.time +\
            "\nurl: " + self.url +\
            "\nscore: " + str(self.score) +\
            "\nterms count: " + str(self.terms)
        ac = 0;
        for i_word in range(len(self.words)):
            if self.freqs[i_word]<10e-6: # 不存在对应单词
                continue
            ac = ac +1
            s = s+'\n------------------------------------------------\n'
            s = s + '\nword: [' + self.words[i_word] + "] freq: " + str(self.freqs[i_word])
            for p_pair in self.positions.setdefault(i_word,list()):
                s = s + '\nposition: ' + str(p_pair)
                s = s + '\n[ ...' + self.doc[max(p_pair[0]-20,0):p_pair[0]+60].replace('\n',' ') + '... ]'
            s = s + '\n'
        s = s + 'accuracy:' + str(ac/len(self.words))
        return s