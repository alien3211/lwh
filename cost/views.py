from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import CmpForm

def index(request):
    if request.method == 'POST':
        form = CmpForm(request.POST)
        if form.is_valid():
            request.session['_data'] = request.POST
            return HttpResponseRedirect(reverse('result'))
    else:
        form = CmpForm()
    return render(request, 'cost/cmp_cost.html',
                  {'form': form}
                  )

def result(request):
    data = request.session.get('_data')

    # Todo: tu dodac logike obliczen w data masz wszystie elementy ktore zdefiniowales w forms.py
    return render(request, 'cost/result.html',
                  {'data': data}
                  )