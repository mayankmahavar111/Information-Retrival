import os
import sqlite3
import progressbar


"""
sql_transaction=[]

def transaction(db ,conn,sql):
    global sql_transaction
    sql_transaction.append(sql)
    if len(sql_transaction) >= 1000:
        db.execute('BEGIN TRANSACTION')
        for s in sql_transaction:
            try:
                db.execute(s)
            except Exception as e:
                pass
        conn.commit()
        sql_transaction = []

def createDocument(db,conn,number):
    for i in range(1,number+1):
        sql= "insert into document_vector VALUES ({},'')".format(i)
        #print sql
        transaction(db,conn,sql)



def createTable(db):
    query='create table if not exists document_vector ( document_id INTEGER NOT NULL  PRIMARY KEY AUTOINCREMENT ,body TEXT );'
    db.execute(query)


def getTfIdf(db,term):
    sql="select tfidf from tfidf where term = '{}'".format(term)
    res=db.execute(sql)
    res=res.fetchone()
    return res[0]



def getTerm(db):
    sql="select term from term"
    res = db.execute(sql)
    res = res.fetchall()
    temp = []
    for x in res:
        temp.append(x[0])
    return temp

def getVector(db,doc_id):
    sql="select body from document_vector where document_id = {}".format(doc_id)
    res=db.execute(sql)
    return res.fetchone()[0]

def updateDocument(db,conn,flag,tfidf):
    tfidf=tfidf.split(',')
    for i in range(len(tfidf)):
        body=getVector(db,i+1)
        if flag == 0:
            body=tfidf[i]
        else:
            body=body+","+tfidf[i]
        sql="update document_vector set body = '{}' where document_id= {}".format(body,i+1)
        transaction(db,conn,sql)


if __name__ == '__main__':
    db_name = 'document'
    conn = sqlite3.connect('{}.db'.format(db_name))
    db = conn.cursor()
    createTable(db)
    createDocument(db,conn,12000)
    term=getTerm(db)
    limit=len(term)
    bar=progressbar.ProgressBar()
    for i in bar(range(limit)):
        tfidf=getTfIdf(db,term[i])
        #print len(tfidf.split(','))
        updateDocument(db,conn,i,tfidf)

    if len(sql_transaction) >0 :
        for s in sql_transaction:
            db.execute(s)
    conn.commit()
"""
