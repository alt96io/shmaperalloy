from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
#from django.views.generic.edit import UpdateView, CreateView
from django.urls import reverse
from django.template.defaultfilters import slugify

from .models import Taskname, Docname
from .forms import SubmissionForm, DocForm, ApprovalForm

def dashboard(request):
    latest_task_list = Taskname.objects.all().order_by('-input_date')
    return render(request, 'report/dashboard.html', {'latest_task_list': latest_task_list})

def dashboard_creator(request):
    document_list = Docname.objects.order_by('-input_date')[:100]
    return render(request, 'report/dashboard_creator.html', {'document_list': document_list})

def create(request):
    form = DocForm(request.POST)
    if request.method == 'POST':
        form = DocForm(request.POST)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.page_slug = slugify(doc.doc_name)
            doc.save()
            document_list = Docname.objects.order_by('-input_date')[:100]
            messages.success(request, ('Document has been created!'))
            return HttpResponseRedirect(reverse('report:documents'))
        else:
            form = DocForm()
            return render(request, 'report/create.html', {'form':form})
    return render(request, 'report/create.html', {'form':form})


def erase(request, page_slug):
    doc = get_object_or_404(Docname, page_slug=page_slug)
    doc.delete()
    document_list = Docname.objects.order_by('-input_date')[:100]
    messages.success(request, ('Document has been deleted.'))
    return HttpResponseRedirect(reverse('report:documents'))

def documents(request):
    document_list = Docname.objects.order_by('-input_date')[:100]
    return render(request, 'report/documents.html', {'document_list': document_list})

def input(request, page_slug):
    doc = get_object_or_404(Docname, page_slug=page_slug)
    if request.method == 'POST':
        form = SubmissionForm(request.POST)
#check whether form is valid
        if form.is_valid():
            task = form.save(commit=False)
            task.docname = doc
            task.save()
            latest_task_list = Taskname.objects.all().order_by('-input_date')
            messages.success(request, ('Submission has been logged!'))
            return HttpResponseRedirect(reverse('report:submissions', args=(doc.page_slug,)))
#            return render(request, 'report/submissions.html', {'latest_task_list': latest_task_list})
#       Always return an HttpResponseRedirect after successfully dealing 
#       with post data.    
    else:
        form = SubmissionForm()
        return render(request, 'report/input.html', {'form': form,'page_slug': page_slug})

    return render(request, 'report/input.html', {'form': form, 'page_slug': page_slug})

def edit(request, pk, page_slug):
    doc = get_object_or_404(Docname, page_slug=page_slug)
    task = get_object_or_404(Taskname, pk=pk)
    if request.method == 'POST':
        form = SubmissionForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            latest_task_list = Taskname.objects.all().order_by('-input_date')
            messages.success(request, ('%s has been edited.' % task.task_name))
            return render(request, 'report/submissions.html', {'page_slug': page_slug, 'latest_task_list': latest_task_list})
    else:
        form = SubmissionForm(instance=task)
        return render(request, 'report/edit.html', {'form':form, 'page_slug': page_slug})
    return render(request, 'report/edit.html', {'form':form, 'page_slug': page_slug})   

def deletion(request, page_slug, pk):
    doc = get_object_or_404(Docname, page_slug=page_slug)
    task = get_object_or_404(Taskname, pk=pk)
    task.delete()
    latest_task_list = Taskname.objects.order_by('-input_date')[:100]
    messages.success(request, ('Submission has been deleted.'))
    return HttpResponseRedirect(reverse('report:submissions', args=(doc.page_slug,)))

def submissions(request, page_slug):
    doc = get_object_or_404(Docname, page_slug=page_slug)
    latest_task_list = Taskname.objects.filter(docname__page_slug=page_slug).order_by('-input_date')[:100]
#    t = get_object_or_404(Taskname, pk=1)
#    t2 = get_object_or_404(Taskname, pk=1)
    if request.method == 'POST':
#        t = get_object_or_404(Taskname, pk=2)
#        for item in request.POST.get('tasks'):
#            t = get_object_or_404(Taskname, pk=item)
#            t.task_status = 1
        form = ApprovalForm(request.POST)
        if 'approve' in request.POST:
#                for item in form.POST.getlist('tasks'):
            for item in form.cleaned_data['tasks']:
                item.task_status = 1
#                t = get_object_or_404(Taskname, pk=item)
#                    t = latest_task_list.filter(pk=item)
#                    t.task_status = 1

    return render(request, 'report/submissions.html', {'page_slug': page_slug, 'doc': doc, 'latest_task_list': latest_task_list})

def profile(request):
    return render(request, 'report/profile.html')

def completed(request):
    return HttpResponse("The following report has been compiled")