from django.contrib.auth.models import User
from django.db.models import Count
from django.contrib import messages
from .models import Task, TaskStatus, Issue, IssueStatus, Project


def update_issue(request, issue):
    issue.task_name = request.POST.get('task_name')
    issue.task_description = request.POST.get('task_description')
    issue.assigned_to = User.objects.get(id=int(request.POST.get('assigned_to')))
    issue.status = IssueStatus.objects.get(status_id=int(request.POST.get('status')))
    issue.save()
    messages.success(request, 'Issue updated successfully.')


def update_task(request, task):
    task.task_name = request.POST.get('task_name')
    task.task_description = request.POST.get('task_description')
    task.assigned_to = User.objects.get(id=int(request.POST.get('assigned_to')))
    task.status = TaskStatus.objects.get(status_id=int(request.POST.get('status')))
    task.save()
    messages.success(request, 'Task updated successfully.')


def get_user_home_data(user):
    recent_projects = Project.objects.filter(
        userproject__user=user).order_by('-created_at')[:3]
    task_counts = (
        Task.objects
        .filter(assigned_to=user)
        .values('status__status_name', 'status__status_id')
        .annotate(count=Count('status'))
    )
    tasks = (
        Task.objects
        .filter(assigned_to=user)
        .values('task_name', 'project__project_name', 'task_id')
    )

    issues = (
        Issue.objects
        .filter(assigned_to=user)
        .values('issue_name', 'project__project_name', 'issue_id')
    )

    return {
        'task_counts': task_counts,
        'tasks': tasks,
        'issues': issues,
        'recent_projects': recent_projects,
    }


def create_task_helper(request):
    project_id = int(request.POST.get('project'))
    project = Project.objects.get(project_id=project_id)
    task_name = request.POST.get('task_name')
    task_description = request.POST.get('task_description')
    assigned_to_id = int(request.POST.get('assigned_to'))
    assigned_user = User.objects.get(id=assigned_to_id)

    status = TaskStatus.objects.get(status_id=1)
    task_owner = request.user

    task = Task.objects.create(
        project=project,
        task_name=task_name,
        task_description=task_description,
        assigned_to=assigned_user,
        status=status,
        task_owner=task_owner
    )
    task.save()


def create_issue_helper(request):
    if request.method == "POST":
        project_id = int(request.POST.get('project'))
        project = Project.objects.get(project_id=project_id)
        issue_name = request.POST.get('issue_name')
        issue_description = request.POST.get('issue_description')
        assigned_to_id = int(request.POST.get('assigned_to'))
        assigned_user = User.objects.get(id=assigned_to_id)
        status = IssueStatus.objects.get(status_id=1)
        issue_owner = request.user

        issue = Issue.objects.create(
            project=project,
            issue_name=issue_name,
            task_description=issue_description,
            assigned_to=assigned_user,
            status=status,
            issue_owner=issue_owner
        )
        issue.save()
        return True  # Indicate success

    return False  # Indicate failure
