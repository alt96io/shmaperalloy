from django import forms
from django.forms import models
from django.utils.translation import gettext_lazy as _
from .models import Taskname, Docname

#Form to create new content for a document
class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Taskname
        fields = ["task_name", "input_contributor", "task_text", "hours_worked"]
        labels = {
            "task_name": _('Section'),
            "task_text": _('Content'),
        }

#Form to create new document
class DocForm(forms.ModelForm):
    class Meta:
        model = Docname
#        fields = ["doc_name", "doc_text", "doc_creator"]
        fields = ["doc_name", "doc_text"]

#customizing ModelChoiceField in Django to have more control over object data
class NewModelChoiceIterator(models.ModelChoiceIterator):
    def choice(self, obj):
        return (self.field.prepare_value(obj),self.field.label_from_instance(obj),obj)

class NewModelChoiceField(models.ModelMultipleChoiceField):
    def _get_choices(self):
        if hasattr(self, '_choices'):
            return self._choices
        return NewModelChoiceIterator(self)

    choices = property(_get_choices, forms.MultipleChoiceField._set_choices)

#create dataset of tasks with checkbox selected
class ApprovalForm(forms.ModelForm):
    tasks = forms.ModelMultipleChoiceField(
#        widget = forms.CheckboxSelectMultiple,
#    )

    #tasks = NewModelChoiceField(
        queryset = Taskname.objects.all(),
        widget = forms.CheckboxSelectMultiple,
    )
