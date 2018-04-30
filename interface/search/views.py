# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from search.forms import querystr
from django.views.generic import View
from django.shortcuts import render,redirect
import sqlite3
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer ,WordNetLemmatizer
import time,math,operator,progressbar
from segmented import segment



query=""
stop = set(stopwords.words('english'))
stemmer = PorterStemmer()
lemma = WordNetLemmatizer()


class index(View):
    form_class=querystr
    template_name='search/search.html'
    def get(self, request):
        form=self.form_class()
        return render(request,self.template_name,{'form':form})

    def post(self, request):
        global query
        form = self.form_class(request.POST)
        #print "hello"
        if form.is_valid():
            query = form.cleaned_data['query']
            bias=form.cleaned_data['engine']
            bias=int(bias)
            #print bias , bias==2
            #print query
            if bias == 2 :
                return redirect('/search/globalresult')
            elif bias==3:
                return redirect('/search/segmentresult')
            elif bias ==4:
                return redirect('/search/generaliseresult')
            else:
                return redirect('/search/result')
        else:
            return render(request, self.template_name, {'form': form})

def connectDb(db_name):
    dir = "G:\\6th sem\\Information-Retrival"
    conn = sqlite3.connect('{}/{}.db'.format(dir, db_name))
    db = conn.cursor()
    return db,conn

def closeDb(db,conn):
    db.close()
    conn.close()

def preprocess(que):
    tokens=word_tokenize(que)
    temp = []
    for token in tokens:
        if token.isalpha() == True and token not in stop:
            temp.append(stemmer.stem(token.lower()))
    query = " ".join(temp)
    return query

def getQueryVector(term):
    que=preprocess(query)
    print que
    temp = []
    # print len(term)
    for x in term:
        test = que.split(" ")
        occur = test.count(x[0])
        # print occur* float(x[1])
        tfidf = str(occur * float(x[1]))
        temp.append(tfidf)
    # print len(temp)
    return ",".join(temp)

def getTerm(db):
    sql="select * from term order by term ASC "
    res = db.execute(sql)
    res = res.fetchall()
    return res

def getMaxDocument(db):
    sql="select max(document_id) from document_vector"
    res=db.execute(sql)
    return res.fetchone()[0]

def getDocumentVector(doc_id,db):
    sql="select body from document_vector WHERE document_id = {}".format(doc_id)
    res=db.execute(sql)
    return res.fetchone()[0]

def getValue(vector):
    feature=vector.split(",")
    value=0
    for x in feature:
        value+=float(x)**2
    value=math.sqrt(value)
    return value

def getCosineSimiliarity(queryVector,documentVector,queryMagn,documentMagn):
    queryVector=queryVector.split(',')
    documentVector=documentVector.split(',')
    value=0
    for i in range(len(queryVector)):
        value+= float(queryVector[i]) * float(documentVector[i])
    return value/(queryMagn*documentMagn)

def getDocuments(queryVector,limit,db):
    queryMagn=getValue(queryVector)

    resul={}
    if queryMagn == 0:
        return resul

    for i in (range(1,limit+1)):
        if i%100==0:
            print i
        documentVector=getDocumentVector(i,db)
        #print "document vector"
        documentMagn=getValue(documentVector)
        #print "document magnitude"
        similiarity=getCosineSimiliarity(queryVector,documentVector,queryMagn,documentMagn)
        #print similiarity
        if similiarity !=0.0:
            resul[i]=similiarity
    return resul

def getBody(db,doc_id):
    sql="select substr(body,1,25) from train  where train_id = {}".format(doc_id)
    #print sql
    res=db.execute(sql)
    return res.fetchone()[0]


def getClick(db,doc_id,position):
    sql ="select body from click where document_id = {}".format(doc_id)
    #print sql
    res=db.execute(sql)
    clicks=res.fetchone()[0]
    return clicks.split(',')[position]

def getGlobalBias(resul,db):
    temp={}
    i=0
    #print resul
    for x in resul:
        click=getClick(db,x[0],i)
        #print x
        bias=float(click)/float(x[1])
        temp[x[0]]=(str(float(x[1]) / float(bias)))
    return temp

def getGeneraliseBias(resul,bias):
    doc=[]
    similiarity=[]
    bi=[]
    for x in resul:
        doc.append(x[0])
        similiarity.append(float(x[1]))
    #print bias
    for x in bias:
        #print x
        bi.append(float(bias[x]))
    temp={}
    for i in range(len(similiarity)):
        value=1/(1+math.e**(similiarity[i]*bi[i]))
        temp[doc[i]]=value
    #print temp
    return temp



def sortResult(resul):
    sorted_result= sorted(resul.items(),key=operator.itemgetter(1),reverse=True)
    return sorted_result

def filterResult(resul):
    temp=[]
    for x in resul:
        temp.append(x[0])
    return temp

def power(resul,tq):
    temp={}
    for x in resul:
        temp[x[0]]= float(x[1]) ** float(tq)
    return temp

def result(request):
    print "normal"
    db,conn=connectDb('document')
    term = getTerm(db)
    limit = 1000
    #print query

    queVector=getQueryVector(term)
    resul=getDocuments(queVector,limit,db)
    #print "got result"
    closeDb(db,conn)

    #print "result "
    resul=sortResult(resul)
    #print resul[:10]
    resul=filterResult(resul)

    db,conn=connectDb('result')
    test={}
    for i in range(len(resul)):
        test[resul[i]] = getBody(db,resul[i])

    time.sleep(1)
    return render(request,'search/result.html',{'res':test})


def globalResult(request):
    print "global"
    db, conn = connectDb('document')
    term = getTerm(db)
    limit = 1000
    #print query

    queVector = getQueryVector(term)
    resul = getDocuments(queVector, limit, db)
    #print "got result"

    resul = sortResult(resul)
    resul=getGlobalBias(resul,db)
    closeDb(db, conn)

    #print "result "
    resul=sortResult(resul)
    #print resul
    resul=filterResult(resul)
    #print resul
    db, conn = connectDb('result')
    test = {}
    for i in range(len(resul)):
        test[resul[i]] = getBody(db, resul[i])

    time.sleep(1)
    return render(request, 'search/result.html', {'res': test})


def segmentResult(request):
    print "segment"
    db, conn = connectDb('document')
    term = getTerm(db)
    limit = 1000
    # print query

    queVector = getQueryVector(term)
    resul = getDocuments(queVector, limit, db)
    # print "got result"

    resul = sortResult(resul)
    resul = getGlobalBias(resul, db)
    resul=sortResult(resul)
    doc_id =filterResult(resul)
    tq=segment(doc_id,db)
    #print tq
    closeDb(db, conn)
    resul=power(resul,tq)
    resul=sortResult(resul)
    resul=filterResult(resul)
    db, conn = connectDb('result')
    test = {}
    for i in range(len(resul)):
        test[resul[i]] = getBody(db, resul[i])

    time.sleep(1)
    return render(request, 'search/result.html', {'res': test})



def generaliseResult(request):
    print "generalise"

    db, conn = connectDb('document')
    term = getTerm(db)
    limit = 1000
    # print query

    queVector = getQueryVector(term)
    resul = getDocuments(queVector, limit, db)
    # print "got result"

    resul = sortResult(resul)
    bias = getGlobalBias(resul, db)
    closeDb(db, conn)
    resul=getGeneraliseBias(resul,bias)
    resul=sortResult(resul)
    #print resul
    resul=filterResult(resul)
    #print resul

    db, conn = connectDb('result')
    test = {}
    for i in range(len(resul)):
        test[resul[i]] = getBody(db, resul[i])

    time.sleep(1)
    return render(request, 'search/result.html', {'res': test})


def incClick(request,doc_id,position):
    doc_id=int(doc_id)
    position=int(position)
    position= position-1
    print doc_id
    print position

    db,conn=connectDb('document')

    sql="select body from click where document_id = {}".format(doc_id)
    time.sleep(1)
    #print sql
    res=db.execute(sql)
    clicks=res.fetchone()[0]

    clicks=clicks.split(',')
    temp=[]
    for i in range(len(clicks)):
        if i == position :
            temp.append(str(int(clicks[i])+1))
        else:
            temp.append(str(clicks[i]))
    temp=",".join(temp)

    sql = "update click set body = '{}' where document_id ={} ".format(temp,doc_id)
    #print sql
    db.execute(sql)
    conn.commit()

    closeDb(db,conn)

    db,conn=connectDb('result')
    sql="select body from train where train_id = {}".format(doc_id)
    res=db.execute(sql)
    body=res.fetchone()[0]

    return render(request, 'search/description.html',{'body' : body})