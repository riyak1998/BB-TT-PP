import math
import time
import pickle
from LDAScript import Model
from math import exp
from gensim.test.utils import datapath
from csvTOsql import connect
class User:
    def __init__(self,id,size):
        self.user_id = id
        self.spikes = [(-math.inf) for i in range(0,size) ]
    def update_spike(self,indices):
        curr_time = int(round(time.time()))
        for i in indices:
            self.spikes[i] = curr_time
    def get_preference_vector(self,curr_time,alpha,min_val):
        l=[]
        for i in range(0,len(self.spikes)):
            l.append((i,min_val + (1-min_val)*exp(-1.0*alpha*(curr_time - self.spikes[i]))))
        return l
class Recommendation:
    __instance=None
    __name = "Recommendation"
    __path = datapath(__name)
    __model = Model.getInstance()
    __alpha = 5.730e-7
    __min_val = 0.1
    def getInstance():
        if Recommendation.__instance==None:
            Recommendation()
        return Recommendation.__instance
    def __init__(self):
        try:
            file = open(Recommendation.__path, 'rb')
            Recommendation.__instance = pickle.load(file)
            file.close()
        except Exception as e:
            print(e)
            conn = connect()
            self.users = {}
            if conn!=None:
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM users")
                rowss = cursor.fetchall()
                for row in rowss:
                    self.users[row[0]] = User(row[0],Recommendation.__model.dimensions)
                cursor.close()
                conn.close()
            file = open(Recommendation.__path, 'wb')
            pickle.dump(self, file, pickle.HIGHEST_PROTOCOL)
            file.close()
            Recommendation.__instance = self
    def add_user(self, id):
        self.users[id] = User(id,Recommendation.__model.dimensions)
        file = open(Recommendation.__path, 'wb')
        pickle.dump(self, file, pickle.HIGHEST_PROTOCOL)
        file.close()
    def show_users(self):
        for index, user in self.users.items():
            print(index,user.spikes)
    def recommend_articles(self,id):
        curr_time = int(round(time.time()))
        return Recommendation.__model.getReccommendation(self.users[id].get_preference_vector(curr_time, Recommendation.__alpha, Recommendation.__min_val))
    def read_articles(self, ids , uid):
        conn = connect()
        indices_set = set()
        if conn!=None:
            cursor = conn.cursor()
            for id in ids:
                cursor.execute("SELECT content from articles where id=" + str(id))
                rows = cursor.fetchall()
                l = Recommendation.__model.getVector(rows[0][0])
                l.sort(key = lambda x: x[1], reverse = True)
                for i in range(0,5):
                    indices_set.add(l[i][0])
            self.users[uid].update_spike(indices_set)
            file = open(Recommendation.__path, 'wb')
            pickle.dump(self, file, pickle.HIGHEST_PROTOCOL)
            file.close()
            return True
        return False            
    def initialize_vec(self, tags, id):
        ans = set()
        sets = {}
        l = Recommendation.__model.model.show_topics(num_topics=50, num_words=5, log=False, formatted=False)
        for i in range(0,Recommendation.__model.dimensions):
            sets[i] = set()
            for j in range(0,5):
                sets[i].add(l[i][1][j][0])
        for tag in tags:
            for k,val in sets.items():
                if tag in val:
                    ans.add(k)
        self.users[id].update_spike(ans)
        file = open(Recommendation.__path, 'wb')
        pickle.dump(self, file, pickle.HIGHEST_PROTOCOL)
        file.close()
