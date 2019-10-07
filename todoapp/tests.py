from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Task, User
from .Handlers.TaskHandler import TaskHandler


class TaskModelTest(TestCase):

    def test_was_created(self):
        user_name = "Alice"
        user = User.objects.create(name=user_name)

        title = "Shopping"
        content = "-buy carrot\n-buy water"
        is_done = False
        date_created = timezone.now()
        task = Task.objects.create(
            title=title,
            content=content,
            is_done=is_done,
            date_created=date_created,
            assignee=user)
        self.assertTrue(isinstance(task, Task))
        task_from_db = Task.objects.get(id=task.id)
        self.assertEqual(task.id, task_from_db.id)


class UserModelTest(TestCase):

    def test_was_created(self):
        user_name = "Alice"
        user = User.objects.create(name=user_name)
        self.assertTrue(isinstance(user, User))
        user_from_db = User.objects.get(id=user.id)
        self.assertEqual(user.name, user_from_db.name)


class TaskIndexViewTest(TestCase):

    def setUp(self):
        user_name = "Alice"
        self.user = User.objects.create(name=user_name)

    def test_no_task(self):
        """Check view returns message: `Nothing to do...`"""
        response = self.client.get(reverse('todoapp:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nothing to do...")
        self.assertQuerysetEqual(response.context['context']['tasks'], [])

    def test_show_one_task(self):
        task = TaskHandler.create_task(self.user)
        response = self.client.get(reverse('todoapp:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(list(
            response.context['context']),
            [task])

    def test_show_two_tasks(self):
        """Check two tasks appears in view"""
        task1 = TaskHandler.create_task(self.user)
        task2 = TaskHandler.create_task(self.user)
        response = self.client.get(reverse('todoapp:index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['context']['tasks']), [task1, task2])

    def test_not_show_task_from_future(self):
        """Do not show tasks with future date"""
        task = TaskHandler.create_task(self.user, days_in_future=5)
        response = self.client.get(reverse('todoapp:index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['context']['tasks']), [])


class UserDetailViewTest(TestCase):

    def setUp(self):
        user_name = "Alice"
        self.user = User.objects.create(name=user_name)

    def test_user_with_no_tasks(self):
        response = self.client.get(reverse('todoapp:user_detail', args=(self.user.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(self.user.task_set.all()), [])
        self.assertContains(response, "No tasks...")

    def test_user_with_1_task(self):
        task = TaskHandler.create_task(self.user)
        response = self.client.get(reverse('todoapp:user_detail', args=(self.user.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(self.user.task_set.all()), [task])
        self.assertContains(response, task)

    def test_incorrect_user(self):
        incorrect_id = 2
        response = self.client.get(reverse('todoapp:user_detail', args=(incorrect_id,)))
        self.assertEqual(response.status_code, 404)

    def test_user_with_3_tasks(self):
        number_of_tasks = 3
        tasks = []
        for i in range(number_of_tasks):
            tasks.append(TaskHandler.create_task(self.user))
        response = self.client.get(reverse('todoapp:user_detail', args=(self.user.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(self.user.task_set.all()), tasks)
        for t in tasks:
            self.assertContains(response, t)

    def test_user_with_2_tasks_in_future(self):
        number_of_tasks = 2
        tasks = [TaskHandler.create_task(self.user, days_in_future=5) for i in range(number_of_tasks)]
        response = self.client.get(reverse('todoapp:user_detail', args=(self.user.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['filtered_tasks']), [])
        self.assertContains(response, "No tasks...")

    def test_user_with_tasks_in_past_and_future(self):
        task_in_future = TaskHandler.create_task(self.user, days_in_future=5)
        task_in_past = TaskHandler.create_task(self.user)
        response = self.client.get(reverse('todoapp:user_detail', args=(self.user.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['filtered_tasks']), [task_in_past])
        self.assertContains(response, task_in_past)


class TaskDetailViewTest(TestCase):

    def setUp(self):
        user_name = "Alice"
        self.user = User.objects.create(name=user_name)

    def test_incorrect_task(self):
        incorrect_id = 2
        response = self.client.get(reverse('todoapp:task_detail', args=(incorrect_id,)))
        self.assertEqual(response.status_code, 404)

    def test_correct_task(self):
        task = TaskHandler.create_task(self.user)
        response = self.client.get(reverse('todoapp:task_detail', args=(task.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, task.title)
        self.assertContains(response, task.content)
        self.assertContains(response, task.is_done)
        self.assertContains(response, task.assignee)