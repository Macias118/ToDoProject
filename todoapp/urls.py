from django.urls import path

from . import views

app_name = 'todoapp'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('task/<int:pk>', views.TaskDetailView.as_view(), name='task_detail'),
    path('user/<int:pk>', views.UserDetailView.as_view(), name='user_detail'),
    path('addItem', views.add, name='addItem'),
    path('deleteItem/<int:task_id>', views.deleteItem, name='deleteItem'),
]