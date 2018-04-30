import sqlite3
import random
import progressbar

sql_transaction=[]

def transaction(db ,conn,sql):
    global sql_transaction
    sql_transaction.append(sql)
    if len(sql_transaction) >= 100:
        db.execute('BEGIN TRANSACTION')
        for s in sql_transaction:
            try:
                db.execute(s)
            except Exception as e:
                pass
        conn.commit()
        sql_transaction = []



def getMaxDocument(db):
    sql="select max(document_id) from document_vector"
    res=db.execute(sql)
    return res.fetchone()[0]

def createTable(db):
    query='create table if not exists click ( document_id INTEGER NOT NULL  PRIMARY KEY AUTOINCREMENT ,body TEXT );'
    db.execute(query)

def insertDocument(db,conn,clicks,doc_id):
    sql="insert into click VALUES ( {} , '{}')".format(doc_id,clicks)
    transaction(db,conn,sql)


if __name__ == '__main__':
    db_name = 'document'
    conn = sqlite3.connect('{}.db'.format(db_name))
    db = conn.cursor()
    limit=getMaxDocument(db)
    createTable(db)
    bar=progressbar.ProgressBar()
    for i in bar(range(1,limit+1)):
        temp=[]
        for j in range(1,limit+1):
            temp.append(str(random.randint(1,limit/2)))
        temp=','.join(temp)
        insertDocument(db,conn,temp,i)


    if len(sql_transaction) > 0:
        for s in sql_transaction:
            db.execute(s)
    conn.commit()


