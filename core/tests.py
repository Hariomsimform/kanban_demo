from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import Project, Task, Issue, TaskStatus, IssueStatus


class CoreViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        issue_status = IssueStatus.objects.create(status_name='Open')
        self.project = Project.objects.create(
            project_name='Test Project', project_description='Test Description',
            created_by=self.user)
        self.task = Task.objects.create(
            project=self.project, task_name='Test Task',
            task_description='Test Task Description',
            assigned_to=self.user,
            status=TaskStatus.objects.create(status_name='Open'),
            task_owner=self.user
        )
        self.issue = Issue.objects.create(
            project=self.project,
            issue_name='Test Issue',
            task_description='Test Issue Description',
            assigned_to=self.user,
            status=issue_status,
            issue_owner=self.user
        )
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

    def test_login(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_home(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)

    def test_complete_profile(self):
        response = self.client.get(reverse('complete_profile'))
        self.assertEqual(response.status_code, 200)

    def test_view_task(self):
        url = reverse('view_task', args=[self.task.task_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_delete_task(self):
        url = reverse('delete_task', args=[self.task.task_id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

    def test_view_issue(self):
        url = reverse('view_issue', args=[self.issue.issue_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_delete_issue(self):
        url = reverse('delete_issue', args=[self.issue.issue_id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

    def test_user_projects(self):
        response = self.client.get(reverse('user_projects'))
        self.assertEqual(response.status_code, 200)

    def test_get_task(self):
        url = reverse('get_task', args=['status_name', 1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_project_tasks(self):
        url = reverse('project_tasks', args=[self.project.project_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_all_tasks(self):
        response = self.client.get(reverse('all_tasks'))
        self.assertEqual(response.status_code, 200)

    def test_all_issues(self):
        response = self.client.get(reverse('all_issues'))
        self.assertEqual(response.status_code, 200)

    def test_create_project(self):
        response = self.client.get(reverse('create_project'))
        self.assertEqual(response.status_code, 200)

    def test_create_task(self):
        response = self.client.get(reverse('create_task'))
        self.assertEqual(response.status_code, 200)

    def test_select_users(self):
        url = reverse('select_users')
        response = self.client.get(url, {'project_id': self.project.project_id})
        self.assertEqual(response.status_code, 200)

    def test_create_issue(self):
        response = self.client.get(reverse('create_issue'))
        self.assertEqual(response.status_code, 200)

    def test_add_developer(self):
        response = self.client.get(reverse('add_developer'))
        self.assertEqual(response.status_code, 200)

    def test_logout_user(self):
        response = self.client.post(reverse('logout_user'))
        self.assertEqual(response.status_code, 302)

    def tearDown(self):
        pass
