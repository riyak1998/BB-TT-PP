from csvTOsql import connect
import csv
def fetchAll():
    conn = connect()
    if conn!=None:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles")
        rowss = cursor.fetchall()
        rows = []
        rows.append(("ID","Title","Author","Tag","Link","Content"))
        for row in rowss:
            rows.append(row)
        cursor.close()
        conn.close()
        return rows
def insertToCsv():
    file_name = "../../data/filtered_data_after_swift.csv"
    with open(file_name, 'w') as csvfile:
        rows=fetchAll()
        csvwriter = csv.writer(csvfile)  
        csvwriter.writerows(rows)
        return True
print(insertToCsv())
    