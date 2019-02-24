from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
#from django.views.generic.edit import UpdateView, CreateView
from django.urls import reverse

from .models import Taskname
from .forms import SubmissionForm

#class SubmissionCreate(CreateView):
#        model = Taskname
#        fields = ['task_name', 'task_text', 'input_contributor', 'hours_worked']

#class SubmissionUpdate(UpdateView):
#    model = Taskname
#    fields = ['task_name', 'task_text', 'input_contributor', 'hours_worked']
#    template_name_suffix = '_edit_form'
#    template_name_suffix = '_update_form'

def dashboard(request):
    latest_task_list = Taskname.objects.order_by('-input_date')[:100]
    return render(request, 'report/dashboard.html', {'latest_task_list': latest_task_list})

def input(request):

    if request.method == 'POST':
        form = SubmissionForm(request.POST)
#check whether form is valid
        if form.is_valid():
            form.save()
            latest_task_list = Taskname.objects.order_by('-input_date')[:100]
            messages.success(request, ('Submission has been logged!'))
            return HttpResponseRedirect(reverse('report:submissions'))
#            return render(request, 'report/submissions.html', {'latest_task_list': latest_task_list})
#       Always return an HttpResponseRedirect after successfully dealing 
#       with post data.    
    else:
        form = SubmissionForm()
        return render(request, 'report/input.html', {'form': form})

    return render(request, 'report/input.html', {'form': form})

def edit(request, pk):
    task = get_object_or_404(Taskname, pk=pk)
    if request.method == 'POST':
        form = SubmissionForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            latest_task_list = Taskname.objects.order_by('-input_date')[:100]
#    task.delete()
            messages.success(request, ('%s has been edited.' % task.task_name))
            return render(request, 'report/submissions.html', {'latest_task_list': latest_task_list})
    else:
        form = SubmissionForm(instance=task)
        return render(request, 'report/edit.html', {'form':form})
    return render(request, 'report/edit.html', {'form':form})   

def submissions(request):
    latest_task_list = Taskname.objects.order_by('-input_date')[:100]
    return render(request, 'report/submissions.html', {'latest_task_list': latest_task_list})

def completed(request):
    return HttpResponse("The following report has been compiled")