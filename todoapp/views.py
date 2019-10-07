from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from django.urls import reverse

from .models import User, Task
from .Handlers.TaskHandler import TaskHandler
from .forms import TaskMakerForm, FormTest


class IndexView(generic.ListView):
    template_name = 'todoapp/index.html'
    context_object_name = 'context'

    def get_queryset(self, **kwargs):
        context = {}
        context['tasks'] = [t for t in Task.objects.all() if t.was_published_in_past()]
        context['users_possible'] = User.objects.all()
        form = TaskMakerForm()
        context['form'] = form
        return context


class TaskDetailView(generic.DetailView):
    model = Task
    template_name = 'todoapp/detail_task.html'


class UserDetailView(generic.DetailView):
    model = User
    template_name = 'todoapp/detail_user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filtered_tasks'] = [task for task in self.object.task_set.all() if task.was_published_in_past()]
        context['user_name'] = self.object.name
        return context


def add(request):
    if request.method == 'GET':
        form = TaskMakerForm()
    elif request.method == 'POST':
        form = TaskMakerForm(request.POST)
        if form.is_valid():
            user_id = request.POST['assignee']
            title = request.POST['title']
            content = request.POST['content']
            user = User.objects.get(id=user_id)
            t = TaskHandler.create_task(
                user,
                title=title,
                content=content)
            t.save()
            return HttpResponseRedirect(reverse('todoapp:index'))
    return render(request, 'todoapp/addItem.html', {'form': form, 'item_added': True})

def deleteItem(request, task_id):
    task = Task.objects.get(pk=task_id).delete()
    return HttpResponseRedirect(reverse('todoapp:index'))
