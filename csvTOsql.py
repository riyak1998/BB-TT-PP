import mysql.connector
from mysql.connector import Error
from python_mysql_dbconfig import read_db_config
import csv
import sys
csv.field_size_limit(sys.maxsize)

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
#article is a tuple in the same order as this query..
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
    file_name = "../../data/database_3.csv"
    with open(file_name, 'r') as csvfile:  
        csvreader = csv.reader(csvfile)  
        next(csvreader)
        articles=[]
        for row in csvreader:
            articles.append(("0",row[2],row[0],row[-1],row[1],row[-2]))
        insert_articles(articles)
    
    