import nltk
import logging
import numpy as np
import string
from gensim import corpora
from gensim import models
from gensim.test.utils import datapath
from nltk.corpus import stopwords
from six import iteritems
from csvTOsql import fetchall,connect
from sklearn.metrics.pairwise import cosine_similarity
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)

def process(test_string):
    # bad = ['`','~','!','@','#','$','%','^','&','*','(',')','_','-','+','=','{','[','}','}','|',':',';','"','<',',','>','.','?','/','0','1','2','3','4','5','6','7','8','9']
    good = set(string.ascii_lowercase).union(set(string.ascii_uppercase).union(set("'")))
    new_string = ""
    for index in range(0,len(test_string)):
        if test_string[index] not in good:
            new_string+=" "
        else:
            new_string+=test_string[index]
    t = len(new_string)
    return new_string[0:t-12]

class MyCorpus:
    __instance = None
    def getInstance():
        if MyCorpus.__instance==None:
            MyCorpus()
        return MyCorpus.__instance
    def __init__(self):
        self.stoplist = set(stopwords.words('english'))
        self.conn = connect()
        self.cursor = self.conn.cursor()
        self.query = "SELECT content FROM articles"
        self.cursor.execute(self.query)
        self.row = self.cursor.fetchone()
        self.name = "final_dictionary_2"
        try:
            self.dictionary = corpora.Dictionary().load(datapath(self.name))
        except:
            self.dictionary = corpora.Dictionary()
            while self.row is not None:
                self.dictionary.add_documents([process(self.row[0]).lower().split()])
                self.row = self.cursor.fetchone()
            self.cursor.execute(self.query)
            self.row = self.cursor.fetchone()
            stop_ids = [
                self.dictionary.token2id[stopword]
                for stopword in self.stoplist
                if stopword in self.dictionary.token2id ]
            once_ids = [tokenid for tokenid, docfreq in iteritems(self.dictionary.dfs) if docfreq == 1]
            self.dictionary.filter_tokens(stop_ids + once_ids)
            self.dictionary.compactify()
            self.dictionary.save(datapath(self.name))
        MyCorpus.__instance = self
    def __iter__(self):
        while True:
            yield self.dictionary.doc2bow(process(self.row[0]).lower().split())    
            self.row = self.cursor.fetchone()
            if self.row is None:
                self.cursor.execute(self.query)
                self.row = self.cursor.fetchone()
                break
    def show(self):
        print(self.dictionary)
    def addDocumentToDictionary(self,doc):
        self.dictionary.add_documents([process(doc).lower().split()])
        self.dictionary.save(datapath(self.name))

class Model:
    __instance=None
    def getInstance():
        if Model.__instance==None:
            Model()
        return Model.__instance
    def __init__(self):
        self.name = "final_model_3"
        self.dimensions = 50
        self.iterations = 400
        self.passes = 50
        self.alhpa = 'auto'
        self.eta = 'auto'
        self.eval_every = 1
        self.corpus = MyCorpus.getInstance()
        try:
            self.model = models.LdaModel.load(datapath(self.name))
        except:
            self.model =  models.ldamulticore.LdaMulticore(self.corpus, id2word=self.corpus.dictionary, eval_every = self.eval_every, num_topics=self.dimensions, iterations=self.iterations, passes=self.passes,minimum_probability =0.0)
            self.model.save(datapath(self.name))
        Model.__instance = self
    def getVector(self,article):
        return self.model[self.corpus.dictionary.doc2bow(process(article).lower().split())]
    def getReccommendation(self,vector):
        index=1
        similarities = []
        b = np.array([i[1] for i in vector]).reshape(1,self.dimensions)
        for bow in self.corpus:
            bb = self.model[bow]
            a = np.array([i[1] for i in bb ]).reshape(1,self.dimensions)
            simi = cosine_similarity(a, b)
            similarities.append((simi[0][0],index))
            index+=1
        similarities.sort(reverse=True)
        l = [s[1] for s in similarities]
        return l
    def reTrain(self):
        self.model =  models.ldamulticore.LdaMulticore(self.corpus, id2word=self.corpus.dictionary, eval_every = self.eval_every, num_topics=self.dimensions, iterations=self.iterations, passes=self.passes,minimum_probability =0.0)
        self.model.save(datapath(self.name))
mymodel = Model.getInstance()
# print(mymodel.model.show_topics(num_topics=50, num_words=5, log=False, formatted=False))
# print(process("it-s"))
# l = fetchall()
# print(process(l[0]).split())
# for s in stopwords:
# cor = MyCorpus.getInstance()