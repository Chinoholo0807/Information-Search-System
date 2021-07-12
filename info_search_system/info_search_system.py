import json

from config import *
import os
from sklearn.feature_extraction.text import CountVectorizer
from collections import defaultdict
from result_item import ResultItem
import numpy as np
import re


class InfoSystem:
    def __init__(self):
        self.doc_names = os.listdir(data_folder)
        print("Try to get the text list ...")
        self.text_list, self.url_list,self.title_list,self.time_list= self.get_doc_list()
        print("Try to get bag ...")
        self.bag, self.cv_fit = self.get_bag()
        print("Try to get generate_inverse_index table...")
        self.inverse_index_table = self.generate_inverse_index()

    def get_doc_list(self):
        """
        获取文档的列表
        :return: 文档列表 []
        """
        text_list = []
        url_list = []
        title_list = []
        time_list = []
        for doc_name in self.doc_names:
            f = open(data_folder + '\\' + doc_name,'r',encoding='utf-8')
            js = json.load(f)
            text_list.append(js['content'])
            url_list.append(js['url'])
            title_list.append(js['title'])
            time_list.append(js['time'])
        return text_list,url_list,title_list,time_list

    def get_bag(self):
        """
        获取词袋数据字典和词频矩阵
        :param text_list:
        :return:
        """
        # 创建词袋数据字典
        cv = CountVectorizer(token_pattern='[A-Za-z]+',
                             analyzer='word',
                             stop_words='english')
        # 拟合数据,得到词频矩阵 cv_fit[i][j]代表第j个词在第i个文本中的词频
        cv_fit = cv.fit_transform(self.text_list)
        return cv, cv_fit

    def generate_inverse_index(self):
        """
        获取倒排索引表
        :param text_list:
        :param bag:
        :param count_array:
        :return:
        """
        count_array = self.cv_fit.toarray()
        inverse_index_dict = defaultdict(list)  # 构造默认值为list的dict，可以直接append
        words = self.bag.get_feature_names()
        for i_text, text_content in enumerate(self.text_list):  # ('I love you') -> (3,'I love you')
            for i_word, word in enumerate(words):  # ('love') ->(4,'love')
                if count_array[i_text][i_word] != 0:  # 存在该word
                    position_list = [m.span() for m in re.finditer(
                        r'\b(%s|%s)\b' % (word, word.capitalize()), text_content)]  # 注意大小写都要匹配
                    # 存储的是word在text_content的位置[(a1,b1),...,(an,bn)]  text_context[a1,b1)= word
                    inverse_index_dict[word].append((i_text, count_array[i_text][i_word], position_list))
        return inverse_index_dict

    def search(self, query_str):
        """
        返回查询结果
        :param query_str:查询token流
        :param inverse_index_dict:倒排索引表
        :param doc_names: 文档的名字列表
        :param text_list:文档列表
        :param cv:
        :param count_array:
        :return: list of ResultItem
        """
        inverse_index_dict=self.inverse_index_table
        doc_names=self.doc_names
        title_list=self.title_list
        url_list=self.url_list
        time_list=self.time_list
        text_list=self.text_list
        count_array=self.cv_fit
        len_docs = len(doc_names)

        word_list = np.unique(
            np.array(list(filter(None,query_str.lower().split(' '))))  # 先转为小写，再分词，再去重
        )
        print('word list: ',word_list)
        len_words = len(word_list)

        coord = np.zeros(len_docs)  # 1.评分因子 文档中匹配的词条个数/查询中所有词条的数量，越多的查询项在一个文档中，说明些文档的匹配程序越高
        for word in word_list:
            if word in inverse_index_dict:
                # print('----' + word + '----inverse index dict')
                # print(inverse_index_dict.get(word))
                for item in inverse_index_dict.get(word):  # item[0]:idx_of_text item[1]:count item[2]:position
                    coord[item[0]] = coord[item[0]] + 1
        coord = coord / len(word_list)

        terms = np.ones(len_docs)  # 文档归一化因子，文档越长该因子越小，同样匹配的文档，比较短的放比较前面。
        for i_doc in range(len_docs):
            terms[i_doc] = count_array[i_doc,].sum()
        norm = 1 / np.power(terms, 0.5)

        sigma = np.zeros(len_docs)  # 文档向量和查询向量点乘 sigma tf(word in doc) * idf(word)^2
        for word in word_list:
            doc_freq = len(inverse_index_dict.setdefault(word, list()))  # 包含该词的文档数
            idf_word = 1 + np.log(len_docs / (1 + doc_freq))  # 该词的idf值（逆文档频率）
            for item in inverse_index_dict.setdefault(word, list()):
                sigma[item[0]] = sigma[item[0]] + np.power(item[1], 0.5) * np.power(idf_word, 2)

        score = coord * sigma * norm  # 最终评定得分

        # 构造返回结果
        results_dict = dict()
        sort_i_doc = np.argsort(-score)
        for i_doc in sort_i_doc:
            if score[i_doc] > 0:
                results_dict[i_doc] = ResultItem(i_doc,
                                                 doc_names[i_doc],
                                                 title_list[i_doc],
                                                 time_list[i_doc],
                                                 url_list[i_doc],
                                                 text_list[i_doc],
                                                 score[i_doc],
                                                 word_list,
                                                 terms[i_doc])
            else:
                break
        for i_word, word in enumerate(word_list):
            for item in inverse_index_dict.setdefault(word, list()):
                i_doc = item[0]
                results_dict[i_doc].freqs[i_word] = item[1]
                results_dict[i_doc].positions[i_word] = item[2]
        results_list = [i for i in results_dict.values()]
        results_list.sort(key=lambda x: -x.score)
        return results_list
