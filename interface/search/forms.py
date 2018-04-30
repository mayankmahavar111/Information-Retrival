from django import forms


bias=(
    (1,("Normal")),
    (2,("global")),
    (3,("segment")),
    (4,("generalise"))
)

class querystr(forms.Form):
    query =  forms.CharField(label='Query',required=True)
    engine = forms.ChoiceField(label='search using', required=True,choices=bias)