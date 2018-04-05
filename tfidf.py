import sqlite3
import math
import progressbar

train_lenght=12000
sql_transaction=[]


def transaction(db ,conn,sql):
    global sql_transaction
    sql_transaction.append(sql)
    if len(sql_transaction) > 100:
        db.execute('BEGIN TRANSACTION')
        for s in sql_transaction:
            try:
                db.execute(s)
            except Exception as e:
                pass
        conn.commit()
        sql_transaction = []


def createTable(table_name,db):
    query="""create table if not exists {} (term text PRIMARY KEY NOT NULL ,tfidf text NOT NULL ); """.format(table_name)
    #print query
    db.execute(query)


def getVocabulary(table_name,db):
    query="""select *  from {};""".format(table_name)
    res=db.execute(query)
    return res.fetchall()

def getBody(table_name,doc_id,db):
    query="""select body from {} where {}_id={};""".format(table_name,table_name,doc_id)
    res=db.execute(query)
    return res.fetchone()[0]


def getTfIdf(term,table_name,idf,db):
    temp=[]
    for i in range(1,train_lenght+1):
        body=getBody(table_name,i,db)
        f=body.count(term)
        if f==0 :
            tf=0
        else:
            tf= math.log(f+1)/math.log(2)
        temp.append(str(tf*idf))
    return ",".join(temp)


def insert_data(table_name,term,tfidf,db,conn):
    try:
        query=""" insert into {} VALUES ("{}","{}")""".format(table_name,term,tfidf)
        transaction(db,conn,query)
    except:
        pass

def finalize(db,conn):
    global sql_transaction
    if len(sql_transaction ) > 0 :
        db.execute('BEGIN TRANSACTION')
        for s in sql_transaction:
            try:
                db.execute(s)
            except Exception as e:
                pass
        conn.commit()


if __name__ == '__main__':
    db_name = 'document'
    table_name = ['train','term','tfidf']
    conn = sqlite3.connect('{}.db'.format(db_name))
    db = conn.cursor()
    createTable(table_name[2],db)
    vocabulary=getVocabulary(table_name[1],db)
    bar=progressbar.ProgressBar()
    for i in bar(range(len(vocabulary))):
        term=vocabulary[i][0]
        idf=float(vocabulary[i][1])
        tfidf=getTfIdf(term,table_name[0],idf,db)
        insert_data(table_name[2],term,tfidf,db,conn)
    finalize(db,conn)