import sqlite3
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

def getBody(db,id):
    sql="select body from train where train_id = {}".format(id)
    res=db.execute(sql)
    return res.fetchone()[0]

def getTerm(db):
    sql="select * from term order by term ASC "
    res = db.execute(sql)
    res = res.fetchall()
    return res

def createTable(db):
    query='create table if not exists document_vector ( document_id INTEGER NOT NULL  PRIMARY KEY AUTOINCREMENT ,body TEXT );'
    db.execute(query)


def getMaxDocument(db):
    sql="select max(train_id) from train"
    res=db.execute(sql)
    return res.fetchone()[0]

def getVector(term,body):
    temp=[]
    #print len(term)
    for x in term:
        test=body.split(" ")
        occur=test.count(x[0])
        #print occur* float(x[1])
        tfidf=str(occur * float(x[1]))
        temp.append(tfidf)
    #print len(temp)
    return ",".join(temp)


def insertDocument(db,conn,vector,doc_id):
    sql="insert into document_vector VALUES ( {} , '{}')".format(doc_id,vector)
    transaction(db,conn,sql)


if __name__ == '__main__':
    db_name = 'document'
    conn = sqlite3.connect('{}.db'.format(db_name))
    db = conn.cursor()
    createTable(db)
    term=getTerm(db)
    #print term[0][0]
    limit=getMaxDocument(db)
    bar=progressbar.ProgressBar()
    for i in bar(range(1,limit+1)):
        body =getBody(db,i)
        #print body
        vector=getVector(term,body)
        #print vector
        insertDocument(db,conn,vector,i)
    if len(sql_transaction) > 0:
        for s in sql_transaction:
            db.execute(s)
    conn.commit()


