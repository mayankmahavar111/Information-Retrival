# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from search.forms import querystr
from django.views.generic import View
from django.shortcuts import render,redirect
import sqlite3

query=""
class index(View):
    form_class=querystr
    template_name='search/search.html'
    def get(self, request):
        form=self.form_class()
        return render(request,self.template_name,{'form':form})

    def post(self, request):
        global query
        form = self.form_class(request.POST)
        print "hello"
        if form.is_valid():
            query = form.cleaned_data['query']
            #print query
            return redirect('/search/result')
        else:
            return render(request, self.template_name, {'form': form})

def result(request):
    print query
    db_name = 'document'
    conn = sqlite3.connect('{}.db'.format(db_name))
    db = conn.cursor()

    sql = """select TRAIN_id from TRAIN where body like "%{}%" """.format(query)


    res = db.execute(sql)

    temp = res.fetchall()
    print temp
    return render(request,'search/result.html')