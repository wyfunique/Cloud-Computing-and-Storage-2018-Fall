import os
#import torndb
#import mysql.connector
import MySQLdb

articles_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "articles")

#db = torndb.Connection("localhost", "news", "root", "root") 
db = MySQLdb.connect(
  host="localhost",
  user="root",
  passwd="root",
  db="news"

)
cur = db.cursor()

interested_info = ["title", "source_url", "url", "tags", "publish_date", "authors", "summary", "text"]

def preprocess(text):
    for i in range(len(text)):
        text[i] = "'" + text[i] + "'"
        #print text[i]

for source in os.listdir(articles_path):
    #print source
    source_path = os.path.join(articles_path, source)
    for article in os.listdir(source_path):
        path = os.path.join(source_path, article)
        f = open(path, 'r')
        text = f.readlines()
        if len(text) <= 1:
            f.close()
            continue
        text = ''.join(text[1:]).replace("'", "").replace("\n","<br />").split('|')[1:]
        text = [article] + text
        preprocess(text)
        #args = {}
        #for i in range(len(interested_info)):
        #    section = interested_info[i]
        #    args[section] = text[i]
        #for item in text:
        #sql = "INSERT INTO article(" + ','.join(interested_info)  + ") VALUES (" + ','.join(text) + ");"
        sql = "INSERT INTO article VALUES (" + ','.join(text) + ");"
        #print sql
        #print args
        #print text
        #print text[-1]
        #raw_input()
        try:
            cur.execute(sql)
            db.commit()
        except Exception as e:
            print str(e)

db.close()
