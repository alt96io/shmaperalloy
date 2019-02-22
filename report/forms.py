from django import forms
from .models import Taskname

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Taskname
        fields = ["task_name", "input_contributor", "task_text", "hours_worked"]

#class SubmissionUpdate(UpdateView):
#    model = Taskname
#    fields = ['task_name', 'task_text', 'input_contributor', 'hours_worked']
#    template_name_suffix = '_edit_form'
