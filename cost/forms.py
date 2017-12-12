from django import forms

class CmpForm(forms.Form):
    polaczenie = forms.CharField(label='Polaczenie', max_length=100)
    czas = forms.CharField(label='Czas', max_length=100)
    koszt = forms.CharField(label='Koszt', max_length=100)
    # ToDo: tu masz dodac potrzebne ci parametry plus validacja jak potrzebujesz liczby to liczby a nie stringi
