from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.views.generic.edit import UpdateView, CreateView
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
#    return HttpResponse("Welcome, Jimmy Bob")
    latest_task_list = Taskname.objects.order_by('-input_date')[:100]
    return render(request, 'report/dashboard.html', {'latest_task_list': latest_task_list})

def input(request):

    form = SubmissionForm()
#    return render(request, 'report/input.html', {'form': form})
    if request.method == 'POST':
        form = SubmissionForm(request.POST)
#check whether form is valid
        if form.is_valid():
            form.save()
            latest_task_list = Taskname.objects.order_by('-input_date')[:100]
#            messages.success(request, ('Submission has been logged!'))
#            return render(request, 'report/submissions.html', {'latest_task_list': latest_task_list})
            return HttpResponse("The form is valid.")
    
    else:
        form = SubmissionForm()
        latest_task_list = Taskname.objects.order_by('-input_date')[:100]
#        return render(request, 'report/input.html', {'latest_task_list': latest_task_list})
        return render(request, 'report/input.html', {'form': form})

    return render(request, 'report/input.html', {'form': form})

#def edit(request, taskname_id):
#    if request.method == 'POST':
#        task = Taskname.objects.get(pk=taskname_id)
#        form = SubmissionForm(task)
#        form = SubmissionUpdate(task)
#        if form.is_valid():
#            form.save()
#            latest_task_list = Taskname.objects.order_by('-input_date')[:100]
#    task.delete()
#            messages.success(request, ('Submission has been edited.'))
#            return redirect('submissions')
#    else:
#        task = Taskname.objects.get(pk=taskname_id)
#        form = SubmissionForm(task)
#        form = SubmissionUpdate(task)
#    return render(request, 'report/edit.html', {'form':form})   


def submissions(request):
    latest_task_list = Taskname.objects.order_by('-input_date')[:100]
    return render(request, 'report/submissions.html', {'latest_task_list': latest_task_list})

def completed(request):
    return HttpResponse("The following report has been compiled")
