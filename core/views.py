from django.contrib.auth import authenticate, login as auth_login
from django.http import HttpResponse
from core.models import Task
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from .models import Task, TaskStatus, UserProject, Issue, Project, IssueStatus, UserDetail
from django.contrib.auth.models import User
from .forms import UserProfileForm, UserProjectForm
from django.views.generic import TemplateView
from django.contrib import messages

class Home(TemplateView):
    template_name = "core/logintest.html"

@login_required(login_url="/login/")
def view_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task = Task.objects.get(pk=task_id)
    project = task.project
    users = User.objects.filter(userproject__project=project)
    status = TaskStatus.objects.all()
    if request.method == 'POST':
        task.task_name = request.POST.get('task_name')
        task.task_description = request.POST.get('task_description')
        task.assigned_to = User.objects.get(id=int(request.POST.get('assigned_to')))
        task.status = TaskStatus.objects.get(status_id=int(request.POST.get('status')))
        task.save()
        return redirect('/')

    return render(request, 'core/task_detail.html', {'task': task, 'users': users, 'task_statuses': status})

@login_required(login_url="/login/")
def view_issue(request, issue_id):
    issue = Issue.objects.get(pk=issue_id)
    project = issue.project
    users = User.objects.filter(userproject__project=project)
    status = TaskStatus.objects.all()
    if request.method == 'POST':
        issue.task_name = request.POST.get('task_name')
        issue.task_description = request.POST.get('task_description')
        issue.assigned_to = User.objects.get(id=int(request.POST.get('assigned_to')))
        issue.status = IssueStatus.objects.get(status_id=int(request.POST.get('status')))
        issue.save()
        return redirect('/')

    return render(request, 'core/task_detail.html', {'task': issue, 'users': users, 'task_statuses': status})


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("/")

        else:
            return render(request, 'core/login.html', {'error_message': 'Invalid credentials'})

    return render(request, template_name="core/login.html")


def complete_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            messages.success(request, 'Profile completed successfully.')
            return redirect('/')  # Redirect to the home page or another appropriate view
    else:
        form = UserProfileForm()

    return render(request, 'core/complete_profile.html', {'form': form})

@login_required(login_url="/login/")
def home(request):
    recent_projects = Project.objects.filter(userproject__user=request.user).order_by('-created_at')[:3]
    task_counts = (
        Task.objects
        .filter(assigned_to=request.user)
        .values('status__status_name', 'status__status_id')
        .annotate(count=Count('status'))
    )
    tasks = (
        Task.objects
        .filter(assigned_to=request.user)
        .values('task_name', 'project__project_name', 'task_id')
    )

    issues = (
        Issue.objects
        .filter(assigned_to=request.user)
        .values('issue_name', 'project__project_name', 'issue_id')
    )
    user_details = UserDetail.objects.filter(user=request.user)
    if not user_details:
        return redirect("/complete-profile/")
    context = {
        'task_counts': task_counts,
        'tasks': tasks,
        'issues': issues,
        'recent_projects': recent_projects,
        'user_details': user_details,
    }
    breakpoint()

    return render(request, template_name="core/home.html", context=context)

def user_projects(request):
    user = request.user
    user_projects = UserProject.objects.filter(user=user).select_related('project')
    projects = []

    for user_project in user_projects:
        project = user_project.project
        project.task_count = Task.objects.filter(project=project).count()
        project.issue_count = Issue.objects.filter(project=project).count()
        projects.append(project)

    return render(request, 'core/user_projects.html', {'projects': projects})

def get_task(request, status_name, status_id):
    tasks = Task.objects.filter(status_id=status_id).select_related('project')
    context = {'tasks': tasks}
    return render(request, 'core/get_tasks.html', context)


@login_required(login_url="/login/")
def project_tasks(request, project_id):
    # Get the project
    project = Project.objects.get(pk=project_id)

    # Get all task statuses
    task_statuses = TaskStatus.objects.all()

    # Fetch tasks for each status for the given project
    tasks_by_status = {}
    for status in task_statuses:
        tasks_by_status[status.status_name] = Task.objects.filter(
            project=project,
            status=status
        ).values('task_name', 'task_description', 'assigned_to__username')

    context = {
        'project': project,
        'tasks_by_status': tasks_by_status,
    }

    return render(request, template_name="core/project_tasks.html", context=context)


def all_tasks(request):
    tasks = (
        Task.objects
        .filter(assigned_to=request.user)
        .values('task_name', 'project__project_name', 'task_id')
    )
    context = {

        "tasks":tasks
        }
    return render(request, template_name="core/tasks.html", context=context)

def all_issues(request):
    issues = ( # need to change query
        Issue.objects
        .filter(assigned_to=request.user)
        .values('issue_name', 'project__project_name', 'issue_id')
    )
    context = {
        "issues":issues
    }
    return render(request, template_name="core/issues.html", context=context)

def create_project(request):
    if request.method=="POST":
        return HttpResponse("Submitted form")
    return render(request, template_name="core/create_project.html")


def create_issue(request):
    if request.method=="POST":
        return HttpResponse("Submitted form")
    return render(request, template_name="core/create_issue.html")


def create_task(request):
    if request.method == "POST":
        project = Project.objects.get(project_id=int(request.POST.get('project')))
        task_name = request.POST.get('task_name')
        task_description = request.POST.get('task_description')
        assigned_to = request.POST.get('assigned_to')
        assigned_user = User.objects.get(id=int(assigned_to))
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
        return redirect('/')
    projects = Project.objects.filter(userproject__user=request.user)
    users = User.objects.all()

    context = {
        'projects': projects,
        'users': users,
    }

    return render(request, template_name="core/create_task.html", context=context)

def create_issue(request):
    if request.method == "POST":
        project = Project.objects.get(project_id=int(request.POST.get('project')))
        issue_name = request.POST.get('issue_name')
        issue_description = request.POST.get('issue_description')
        assigned_to = request.POST.get('assigned_to')
        assigned_user = User.objects.get(id=int(assigned_to))
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
        return redirect('/')
    
    projects = Project.objects.all()
    users = User.objects.all()

    context = {
        'projects': projects,
        'users': users,
    }

    return render(request, template_name="core/create_issue.html", context=context)


def add_developer(request):
    if request.method == 'POST':
        form = UserProjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Developer added to the project successfully.')
            return redirect('/')
    else:
        form = UserProjectForm()

    return render(request, 'core/userproject.html', {'form': form})
