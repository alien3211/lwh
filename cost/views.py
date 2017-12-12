# from django.http import HttpResponseRedirect
# from django.shortcuts import render
# from django.urls import reverse
#
# from .forms import CmpForm

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

    #przyklad inputu
    lista = [Task(1, 2, 8, 8, 220, 280),
             Task(1, 4, 10, 5, 100, 150),
             Task(2, 3, 6, 4, 300, 400),
             Task(3, 6, 12, 10, 260, 300),
             Task(4, 5, 15, 15, 150, 150),
             Task(5, 6, 10, 2, 200, 360),
             ]

    save = 0

    # wywolanie funkcji
    # *wynik*: czynnosci po redukcji
    wynik = reduce(lista)
    for task in wynik:
        save += task.saved
    # *save*: laczne koszty przyspieszenia
    print(save)

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


def reduce(listt):
    # print("Enter!")
    nodes = []
    crit_paths = find_critical_paths(listt)
    # print(listt)
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
            reduce(listt)
            break

    return listt
