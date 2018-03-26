from django import forms

class querystr(forms.Form):
    query =  forms.CharField(label='Query',required=True)