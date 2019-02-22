import datetime

from django.db import models
from django.utils import timezone
from django.urls import reverse

class Taskname(models.Model):
    task_name = models.CharField(max_length=200)
    task_text = models.TextField('submission')
    input_contributor = models.CharField(max_length=40)
    edit_contributor = models.CharField(max_length=40, default="None")
    hours_worked = models.DecimalField(max_digits=4, decimal_places=1)
    input_date = models.DateTimeField(default=timezone.now)
    edit_date = models.DateTimeField(default=timezone.now)

    # Represent status of project. Could create custom Model Field.
    NOTSTARTED = 0
    INPROGRESS = 1
    COMPLETE = 2
    STATUS_CHOICES = (
        (NOTSTARTED, 'Not Started'),
        (INPROGRESS, 'In Progress'),
        (COMPLETE, 'Complete'),
    )
    task_status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=0,
    )

    def get_absolute_url(self):
        return reverse('submissions', kwargs={'id': self.id})

    def __str__(self):
        return self.task_name + '|' + self.task_text + '|' + self.input_contributor + '|' + str(self.hours_worked)
