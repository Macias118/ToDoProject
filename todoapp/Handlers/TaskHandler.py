import datetime

from django.utils import timezone

from ..models import Task
from .StringHandler import StringHandler


class TaskHandler:

    @staticmethod
    def create_task(assignee, title=StringHandler.get_random_string(), content=StringHandler.get_random_string(16), is_done=False, days_in_future=0):
        time = timezone.now() + datetime.timedelta(days=days_in_future)
        return Task.objects.create(
            title=title,
            content=content,
            is_done=is_done,
            date_created=time,
            assignee=assignee)
