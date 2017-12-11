from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from collections import namedtuple

from .forms import CmpForm

task = namedtuple('Task'['start', 'end', 't-n', 't-gr', 'K-n', 'K-gr'])

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

def find_critical_paths(tasks):
    
    nodes = []    

    unfinished_paths = []    

    tasks = sorted(tasks, key=lambda x: x.a, reverse=True)


    path = [tasks[0]]
    for taskk in tasks:
	# jesli koniec itemu jest poczatkiem ostatniego w path
    	if taskk.end == path[[-1].start:
	    # zobacz, czy nie ma innych w tej samej linii
	    brothers = []
            number_of_brothers = 0
	        for new_task in tasks:
                    if new_task.end == taskk.end and new_task is not taskk:
                        number_of_brothers += 1
		        brothers.append(new_task)
            if number_of_brothers != 0:
                for brother in brothers:
		    copy_path = list(path)
		    copy_path.append(brother)
		    unfinished_paths.append(copy_path)
	    path.append(taskk)
                
        
