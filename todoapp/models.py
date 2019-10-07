from django.utils import timezone
from django.db import models


class User(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Task(models.Model):

    assignee = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=1000)
    is_done = models.BooleanField(default=False)
    date_created = models.DateTimeField('date created')

    def __str__(self):
        return "{} - {}".format(self.title, self.assignee)

    def was_published_in_past(self):
        now = timezone.now()
        return self.date_created <= now
