from django.db import models
from django.contrib.auth.models import User


class UserTechnology(models.Model):
    user_technology_id = models.AutoField(primary_key=True)
    technology_name = models.CharField(max_length=255)
    def __str__(self):
        return self.technology_name

class UserRole(models.Model):
    user_role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=255)
    def __str__(self):
        return self.role_name

class UserDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_role = models.ForeignKey(UserRole, on_delete=models.CASCADE)
    user_technology = models.ForeignKey(UserTechnology, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=255)
    project_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.project_name


class UserProject(models.Model):
    user_project_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)


class UserTask(models.Model):
    user_task_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey('Task', on_delete=models.CASCADE)


class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=255)
    task_description = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.ForeignKey('TaskStatus', on_delete=models.CASCADE)
    task_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner_tasks')

    def __str__(self):
        return self.task_name


class Issue(models.Model):
    issue_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    issue_name = models.CharField(max_length=255)
    task_description = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.ForeignKey('IssueStatus', on_delete=models.CASCADE)
    issue_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner_issues')
    
    def __str__(self):
        return self.issue_name


class IssueStatus(models.Model):
    status_id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.status_name


class TaskStatus(models.Model):
    status_id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.status_name
