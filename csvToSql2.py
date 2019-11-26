import mysql.connector
from mysql.connector import Error
from python_mysql_dbconfig import read_db_config
import csv
import sys
from trial import isWord
csv.field_size_limit(sys.maxsize)
def process(test_string):
    bad = ['`','~','!','@','#','$','%','^','&','*','(',')','_','-','+','=','{','[','}','}','|',':',';','"','<',',','>','.','?','/','0','1','2','3','4','5','6','7','8','9']
    for i in bad: 
        test_string = test_string.replace(i, ' ') 
    return test_string

def connect():
    db_config = read_db_config()
    conn = None
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            print('Connected to MySQL database')
            return conn
    except Error as e:
        print(e)
        return None

def insert_articles(articles):
    query =  "INSERT INTO articles(id,title,author,tag,link,content) " \
            "VALUES(%s,%s,%s,%s,%s,%s)"
    conn = connect()
    if conn!=None:
        try:
            cursor = conn.cursor()
            cursor.executemany(query, articles)
            conn.commit()
        except Error as e:
            print("Error : ",e)
        finally:
            cursor.close()
            conn.close()
def insert_article(article):
    query =  "INSERT INTO articles(id,title,author,tag,link,content) " \
            "VALUES(%s,%s,%s,%s,%s,%s)"
    conn = connect()
    if conn!=None:
        try:
            cursor = conn.cursor()
            cursor.execut(query, article)
            conn.commit()
        except Error as e:
            print("Error : ",e)
        finally:
            cursor.close()
            conn.close()
def fetchall():
    conn = connect()
    if conn!=None:
        cursor = conn.cursor()
        cursor.execute("SELECT content FROM articles")
        rowss = cursor.fetchall()
        rows = []
        for row in rowss:
            rows.append(row[0])
        return rows
        

if __name__ == '__main__':
    file_name = "../../data/scraped_db_2.csv"
    with open(file_name, 'r') as csvfile:  
        csvreader = csv.reader(csvfile)  
        next(csvreader)
        articles=[]
        t=0
        for row in csvreader:
            st = process(row[-2])
            if(len(st)>500):
                if len(st)<3000:
                    if isWord(st):
                        articles.append(("0",row[2],row[0],row[-1],row[1],row[-2]))
                else:
                    if isWord(st[0:3000]):
                        articles.append(("0",row[2],row[0],row[-1],row[1],row[-2]))
        insert_articles(articles)
