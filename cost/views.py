from collections import OrderedDict

from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import CmpForm


class Task(object):
    def __init__(self, start, end, tn, tgr, Kn, Kgr):
        self.start = start
        self.end = end
        self.tn = tn
        self.tgr = tgr
        self.Kn = Kn
        self.Kgr = Kgr
        self.reduced = False
        self.saved = 0
        if self.tn == self.tgr:
            self.gradient = 0
        else:
            self.gradient = (self.Kgr - self.Kn) / (self.tn - self.tgr)

    def __repr__(self):
        return "Task(%s,%s,%s,%s,%s,%s,%s)" % (self.start,
        self.end,
        self.tn ,
        self.tgr,
        self.Kn,
        self.Kgr,
        self.gradient)

    def to_dict(self):
        return OrderedDict(
            ('start', self.start),
            ('end', self.end),
            ('tn', self.tn),
            ('tgr', self.tgr),
            ('Kn', self.Kn),
            ('Kgr', self.Kgr),
            ('gradient', self.gradient)
        )


def result(request):
    data = request.session.get('_data')

    # #przyklad inputu
    # lista = [Task(1, 2, 8, 8, 220, 280),
    #          Task(1, 4, 10, 5, 100, 150),
    #          Task(2, 3, 6, 4, 300, 400),
    #          Task(3, 6, 12, 10, 260, 300),
    #          Task(4, 5, 15, 15, 150, 150),
    #          Task(5, 6, 10, 2, 200, 360),
    #          ]

    return render(request, 'cost/result.html',
                  {'data': data}
                  )

def find_critical_paths(tasks):
    tasks = sorted(tasks, key=lambda x: x.end, reverse=True)

    brothers = [tasks[0]]

    critical_paths = []                                  

    paths = [[tasks[0]]]
    for path in paths:
        orig_path = path
        
        for taskk in tasks:
            if taskk is path[-1]:
                next
            if taskk.end == path[-1].end and taskk not in brothers:
                if len(orig_path) > 1:
                    paths.append(orig_path[:-1].append(taskk))
                else:
                    paths.append([taskk])
                brothers.append(taskk)
                next
            if taskk.end == path[-1].start:
                path.append(taskk)
    # print("paths: ", paths)
    miin = 0
    for path in paths:
        # print("path: ", path)
        time = 0
        for task in path:
            time += task.tn
        if time > miin:
            critical_paths = [path]
            miin = time
        elif time == miin:
            critical_paths.append(path)

    return critical_paths



def index(request):
    """
    Allows a user to update their own profile.
    """

    # Create the formset, specifying the form and formset we want to use.
    LinkFormSet = formset_factory(CmpForm)


    if request.method == 'POST':

        link_formset = LinkFormSet(request.POST)

        if  link_formset.is_valid():

            list_tasks = []
            for link_form in link_formset:
                start = link_form.cleaned_data.get('start')
                end = link_form.cleaned_data.get('end')
                tn = link_form.cleaned_data.get('tn')
                tgr = link_form.cleaned_data.get('tgr')
                Kn = link_form.cleaned_data.get('Kn')
                Kgr = link_form.cleaned_data.get('Kgr')
                list_tasks.append(Task(start, end, tn, tgr, Kn, Kgr))

            save = 0
            critical_paths = []
            wynik = reduce(list_tasks, critical_paths)
            for task in wynik:
                save += task.saved

            request.session['_data'] = {
                'save': save,
                'critical_paths': [list(map(vars, x[0])) for x in critical_paths], # get all vars from task object [[[],[]], [[],[]]]
                'keys': ['start', 'end', 'tn', 'tgr', 'Kn', 'Kgr', 'gradient']
            }
            return HttpResponseRedirect(reverse('result'))

    else:
        link_formset = LinkFormSet()

    context = {
        'link_formset': link_formset,
    }

    return render(request, 'cost/cmp_cost.html', context)

def reduce(listt, critical_paths):
    # print("Enter!")
    nodes = []
    crit_paths = find_critical_paths(listt)
    critical_paths.append(crit_paths)
    print(crit_paths)
    # print(crit_paths)
    # print("------------------")
    for path in crit_paths:
        for task in path:
            nodes.append(task)

    tasks_by_gradient = sorted(nodes, key=lambda x: x.gradient, reverse=False)
    for task in tasks_by_gradient:
        # print(task.gradient, task.reduced)
        if task.gradient != 0 and task.reduced is False:
            task.reduced = True
            task.saved = (task.tn - task.tgr) * task.gradient
            task.tn = task.tgr
            reduce(listt, critical_paths)
            break

    return listt
