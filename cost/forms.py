from django import forms

class CmpForm(forms.Form):
    cos = forms.CharField(label='Your name', max_length=100)
    tam = forms.CharField(label='tam', max_length=100)
    # ToDo: tu masz dodac potrzebne ci parametry plus validacja jak potrzebujesz liczby to liczby a nie stringi
