import sqlite3
import math

def segment(doc,db):

    cat=[]
    #print doc
    for i in range(len(doc)):
        sql="""select category_id from feature where document_id=={} and title=='TRAIN' """.format(doc[i])
        res=db.execute(sql)
        temp=res.fetchall()
        #print doc[i],temp
        for j in temp:
            cat.append(j[0])

    cat1=list(set(cat))

    iqf=[]
    for i in cat1:
        count=cat.count(i)
        val=10/float(count)
        iqf.append(round(math.log(val,2),6))

    #print iqf
    tq=max(iqf)
    #print tq
    return tq


#segment()