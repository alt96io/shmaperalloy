import datetime

from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.template.defaultfilters import slugify
#from django.contrib.auth.models import User
from accounts.models import Member

class Docname(models.Model):
    doc_name = models.CharField(max_length=50)
    doc_text = models.TextField(max_length=250, blank=True)
#    doc_creator = models.CharField(max_length=40)
    doc_creator = models.ForeignKey(Member, on_delete=models.PROTECT)
    input_date = models.DateTimeField(default=timezone.now)
    page_slug = models.SlugField()

    def __str__(self):
        return self.doc_name

class Taskname(models.Model):
    docname = models.ForeignKey(Docname, on_delete=models.CASCADE, default=1)
    task_name = models.CharField(max_length=200)
    task_text = models.TextField('submission')
#    input_contributor = models.CharField(max_length=40)
    input_contributor = models.ForeignKey(Member, on_delete=models.PROTECT)
#    edit_contributor = models.CharField(max_length=40, default="None")
#    edit_contributor = models.ForeignKey(Member, null=True, on_delete=models.SET_NULL)
    hours_worked = models.DecimalField(max_digits=4, decimal_places=1)
    input_date = models.DateTimeField(default=timezone.now)
    edit_date = models.DateTimeField(default=timezone.now)

    # Represent status of comment. Could create custom Model Field.
    SUBMITTED = 0
    APPROVED = 1
    DISAPPROVED = 2
    STATUS_CHOICES = (
        (SUBMITTED, 'Submitted'),
        (APPROVED, 'Approved'),
        (DISAPPROVED, 'Disapproved'),
    )
    task_status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=0,
    )

    def get_absolute_url(self):
        return reverse('submissions', kwargs={'id': self.id})

    def __str__(self):
        return self.task_name + '|' + self.task_text + '|' + self.input_contributor + '|' + str(self.hours_worked)
