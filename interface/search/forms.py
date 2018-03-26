from django import forms

class query(forms.ModelForm):
    class Meta:
        fields=('query')