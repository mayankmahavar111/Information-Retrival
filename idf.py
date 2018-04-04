import sqlite3
import math
import progressbar

sql_transaction=[]


def transaction(db ,conn,sql):
    global sql_transaction
    sql_transaction.append(sql)
    if len(sql_transaction) > 1000:
        db.execute('BEGIN TRANSACTION')
        for s in sql_transaction:
            try:
                db.execute(s)
            except Exception as e:
                pass
        conn.commit()
        sql_transaction = []


def createTable(db,conn,table_name):
    query='create table if not exists {} ( term text PRIMARY KEY , idf FLOAT NOT NULL DEFAULT 0);'.format(table_name)
    #print query
    db.execute(query)
    conn.commit()


def getBody(table_name,db):
    query="""select body from {} limit 12000 """.format(table_name)
    res = db.execute(query)
    temp=res.fetchall()
    res=[]
    for x in temp:
        res.append(x[0])
    return (res)

def getCount(table_name,term,db):
    query="""select count(body) from {} where body like "%{}%" limit 12000 """.format(table_name,term)
    res=db.execute(query)
    return float(res.fetchone()[0])



def insert_data(table_name,term,idf,db,conn):
    try:
        query="""insert into {} values("{}",{})""".format(table_name,term,idf)
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
    table_name = ['train','term']
    conn = sqlite3.connect('{}.db'.format(db_name))
    db = conn.cursor()
    createTable(db,conn,table_name[1])
    corpse=getBody(table_name[0],db)
    vocabulary = " ".join(corpse)
    vocabulary=vocabulary.split(" ")
    vocabulary=list(set(vocabulary))
    #print len(vocabulary)
    N=float(12000)
    bar=progressbar.ProgressBar()
    for i in bar(range(len(vocabulary))):
        term=vocabulary[i]
        n=getCount(table_name[0],term,db)
        if n!=0 :
            idf= math.log(N/n) / math.log(2)
        else:
            idf=0
        insert_data(table_name[1],term,idf,db,conn)
    finalize(db,conn)


    pass
