import csv
import nltk
import logging
from gensim import corpora
from gensim import models
from gensim.test.utils import datapath
from nltk.corpus import stopwords
from six import iteritems
# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
def process(test_string):
    bad = ['`','~','!','@','#','$','%','^','&','*','(',')','_','-','+','=','{','[','}','}','|',':',';','"','<',',','>','.','?','/','0','1','2','3','4','5','6','7','8','9']
    for i in bad: 
        test_string = test_string.replace(i, '') 
    return test_string
class MyCorpus:
    def __init__(self):
        self.stoplist = set(stopwords.words('english'))
        self.fields = []
        self.file_name = "../../data/articles.csv"
        with open(self.file_name, 'r') as csvfile:  
            csvreader = csv.reader(csvfile)  
            self.fields = next(csvreader)
            self.dictionary = corpora.Dictionary(process(row[-1]).lower().split() for row in csvreader) 
            stop_ids = [
                self.dictionary.token2id[stopword]
                for stopword in self.stoplist
                if stopword in self.dictionary.token2id
            ]
            once_ids = [tokenid for tokenid, docfreq in iteritems(self.dictionary.dfs) if docfreq == 1]
            print(len(stop_ids)+len(once_ids))
            self.dictionary.filter_tokens(stop_ids + once_ids)  # remove stop words and words that appear only once
            self.dictionary.compactify()
    def __iter__(self):
        with open(self.file_name,'r') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)
            for row in csvreader:
                yield self.dictionary.doc2bow(process(row[-1]).lower().split())
    def show(self):
        print(self.fields)
        print(self.dictionary)
class Model:
    instance=None
    def getInstance():
        if(instance==None)
            Model()
        return Model.instance
    def __init(self):
        self.corpus = MyCorpus()
        self.model = models.ldamulticore.LdaMulticore(self.corpus, id2word=self.corpus.dictionary, num_topics=20, passes=20)
        Model.instance = self

mycorpus = MyCorpus()
model = models.ldamulticore.LdaMulticore(mycorpus, id2word=mycorpus.dictionary, num_topics=20, passes=20)
temp_file = datapath("model")
model.save(temp_file)
lda = models.LdaModel.load(temp_file)

