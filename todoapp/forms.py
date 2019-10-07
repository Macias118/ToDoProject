from django import forms
from .models import Task


class TaskMakerForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'content', 'assignee')


class FormTest(forms.Form):
    name = forms.CharField(label='Enter ya name:', max_length=10)
    test_amount = forms.IntegerField(label='Give me ya money')
