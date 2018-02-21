import sqlite3
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer ,WordNetLemmatizer


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



def getLength(table_name,db):
    query="""select count(*) from {};""".format(table_name)
    res=db.execute(query)
    return int(res.fetchone()[0])

def getBody(table_name,doc_id,db):
    query="""select body from {} where {}_id = {}""".format(table_name,table_name,doc_id)
    res = db.execute(query)
    return str(res.fetchone()[0])

def update_data(table_name,body,doc_id,db,conn):
    try:
        query="""update {} set body= "{}" where {}_id = {};""".format(table_name,body,table_name,doc_id)
        transaction(db,conn,query)
    except Exception as e :
        print e



if __name__ == '__main__':
    stop = set(stopwords.words('english'))
    stemmer = PorterStemmer()
    lemma = WordNetLemmatizer()
    db_name = 'document'
    table_name='train'
    conn = sqlite3.connect('{}.db'.format(db_name))
    db = conn.cursor()
    length=getLength(table_name,db)+1
    for i in range(1,length):
        if i%1000 == 0:
            print i
        body=getBody(table_name,i,db)
        tokens=word_tokenize(body)
        temp=[]
        for token in tokens:
            if token.isalpha() == True:
                temp.append(stemmer.stem(token.lower()))
        body=" ".join(temp)
        update_data(table_name,body,i,db,conn)



