import sqlite3
import re

sql_transaction=[]
sql_relation_transaction=[]

def createTable(db,table_name):
    query='create table if not exists {} ( {}_id INTEGER NOT NULL  PRIMARY KEY AUTOINCREMENT ,body TEXT );'.format(table_name,table_name)
    #print query
    db.execute(query)

def createRelationship(db,table_name):
    query="""create table if not exists {} (document_id INTEGER NOT NULL , category_id INTEGER  NOT NULL ,title TEXT NOT  NULL ,PRIMARY KEY (document_id,category_id,title));""".format(table_name)
    db.execute(query)




def insert_data(table_name,body,rel,db,conn):
    try:
        query_table="""INSERT INTO {} ( body) VALUES ("{}");""".format(table_name,body)
        transaction_bldr_table(db,conn,query_table,rel)
    except Exception as e:
        #print "inside insert data table ,{}".format(str(e))
        pass


def check(table_name,body,db,conn):
    try:
        sql="""select * from {} where body='{}'""".format(table_name,body)
        res=db.execute(sql)
        if len(res.fetchall()) == 0 :
            return True
        else:
            return False
    except Exception as e:
        pass
        #print('check file  name',str(e))



def transaction_bldr_table(db,conn,sql,rel):
    global sql_transaction
    global sql_relation_transaction
    sql_transaction.append(sql)
    if rel !=None:
        sql_relation_transaction.append(rel)
    if len(sql_transaction) > 1000:
        db.execute('BEGIN TRANSACTION')
        for s in sql_transaction:
            try:
                db.execute(s)
            except :
                pass
        conn.commit()
        sql_transaction = []
        transaction_bldr_relation(db,conn)

def getId(db,table_name,body):
    query="""select {}_id from {} where body = "{}" ;""".format(table_name,table_name,body)

    res=db.execute(query)
    temp=res.fetchone()[0]
    return int(temp)


def getRelationDetails(rel,db):
    test=[]
    for x in rel:
        try:
            temp=x.split('~^')
            table_name=temp[0]
            category=temp[1]
            body=temp[2]
            doc_id=getId(db,table_name,body)
            for categ in category.split(','):
                cat_id=getId(db,'category',categ)
                sql="""insert into feature values({},{},"{}")""".format(doc_id,cat_id,table_name)
                test.append(sql)
        except Exception as e:
            pass
    return test




def transaction_bldr_relation(db ,conn):
    global sql_relation_transaction
    transaction=getRelationDetails(sql_relation_transaction,db)
    #print len(transaction)
    if len(transaction) > 1000:
        db.execute('BEGIN TRANSACTION')
        for s in transaction:
            try:
                db.execute(s)
            except Exception as e:
                pass
        conn.commit()
        sql_relation_transaction = []



if __name__ == '__main__':
    db_name = 'document'
    conn = sqlite3.connect('{}.db'.format(db_name))
    db = conn.cursor()
    corpus_loc= 'reuters'
    tables = ['TRAIN', 'TEST', 'NOT_USED','category']
    relations=['feature']
    for table in tables:
        createTable(db,table)
    for relation in relations:
        createRelationship(db,relation)

    with open('{}\\all-topics-strings.lc.txt'.format(corpus_loc),'r') as f:
        for x in f.readlines():
            temp=x.split('\n')[0]
            if check(tables[3],temp,db,conn) == True:
                insert_data(tables[3],temp,None,db,conn)

    for j in range(22):
        if j > 9 :
            f = open('{}\\reut2-0{}.sgm'.format(corpus_loc,str(j)), 'r')
        else:
            f= open('{}\\reut2-00{}.sgm'.format(corpus_loc,str(j)), 'r')
        lines = f.read()
        lines = re.split('<BODY>|</BODY>', lines)
        print j
        for i in range(len(lines)):
            if i % 2 == 1:
                continue
            if i == len(lines) - 1:
                break
            ab = re.split('<TOPICS>|</TOPICS>', lines[i])[1]
            ab = re.split('<D>|</D>', ab)[1::2]
            category=[]
            if len(ab) == 0:
                category.append('other')
            else:
                for x in ab:
                    category.append(x)
            category=",".join(category)
            table_name = lines[i].split('LEWISSPLIT="')[1]
            table_name = table_name.split('"')[0]
            if table_name == "NOT-USED":
                table_name="NOT_USED"
            lines[i+1] = lines[i+1].split('"')
            lines[i+1] = "".join(lines[i+1])
            lines[i + 1] = lines[i + 1].split("'")
            lines[i + 1] = "".join(lines[i + 1])
            rel=table_name+"~^"+category+"~^"+lines[i+1]
            if check(table_name,lines[i+1],db,conn) == True:
                insert_data(table_name,lines[i+1],rel,db,conn)







