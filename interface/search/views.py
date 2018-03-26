# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from search.forms import query
from search.forms import query
from django.shortcuts import render

from django.shortcuts import render

def index(request):
    if request.method == 'GET':
        form=query
        return render(request,self.template_name,{'form':form})

    else:
        print "hello"
        form = self.form_class(request.POST)
        print "hello"
        query=form.cleaned_data['query']
        return render(request, self.template_name, {'form': form})