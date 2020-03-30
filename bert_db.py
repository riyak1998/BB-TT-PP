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

def fetchall():
    conn = connect()
    if conn!=None:
        cursor = conn.cursor()
        cursor.execute("SELECT id,tag,content FROM articles where tag='")
        rowss = cursor.fetchall()
        rows = []
        rows.append(['ID','Tag','Content'])
        for row in rowss:
            rows.append([row[0],row[1],row[2]])
        return rows

def insertToCsv():
    file_name = "../../data/bert_db_filtered.csv"
    with open(file_name, 'w') as csvfile:
        rows=fetchall()
        csvwriter = csv.writer(csvfile)  
        csvwriter.writerows(rows)
        return True
    
print(insertToCsv())
