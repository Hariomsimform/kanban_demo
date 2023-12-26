from django.contrib.auth import authenticate, login as auth_login, logout
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Task, TaskStatus, UserProject, Issue, Project, UserDetail
from django.contrib.auth.models import User
from .forms import UserProfileForm, UserProjectForm
from django.contrib import messages
from .utils import (update_task,
                    update_issue, get_user_home_data,
                    create_task_helper,
                    create_issue_helper
                    )
from django.http import HttpResponseForbidden


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("/")
        else:
            return render(request,
                          'core/login.html',
                          {'error_message': 'Invalid credentials'})

    return render(request, template_name="core/login.html")


@login_required(login_url="/login/")
def home(request):
    user_details = UserDetail.objects.filter(user=request.user)
    if not user_details:
        return redirect("/complete-profile/")

    context = get_user_home_data(request.user)
    context['user_details'] = user_details

    return render(request, template_name="core/home.html", context=context)


@login_required(login_url="/login/")
def complete_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            messages.success(request, 'Profile completed successfully.')
            return redirect('/')
    else:
        form = UserProfileForm()

    return render(request, 'core/complete_profile.html', {'form': form})


@login_required(login_url="/login/")
def view_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    users = User.objects.filter(userproject__project=task.project)
    status = TaskStatus.objects.all()
    if request.user != task.task_owner and request.user != task.assigned_to:
        return HttpResponseForbidden("You don't have permission to view this task.")

    if request.method == 'POST':
        update_task(request, task)
        return redirect('/')

    return render(
        request,
        'core/task_detail.html',
        {'task': task, 'users': users, 'task_statuses': status})


@login_required(login_url="/login/")
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.user != task.task_owner:
        return HttpResponseForbidden("You don't have permission to delete this task.")
    task.delete()
    return redirect('/')


@login_required(login_url="/login/")
def view_issue(request, issue_id):
    issue = get_object_or_404(Issue, pk=issue_id)
    project = issue.project
    users = User.objects.filter(userproject__project=project)
    status = TaskStatus.objects.all()
    if request.user != issue.issue_owner and request.user != issue.assigned_to:
        return HttpResponseForbidden("You don't have permission to view this issue.")
    if request.method == 'POST':
        update_issue(request, issue)
        return redirect('/')

    return render(
        request,
        'core/task_detail.html',
        {
            'task': issue,
            'users': users,
            'task_statuses': status
        }
    )


@login_required(login_url="/login/")
def delete_issue(request, issue_id):
    issue = get_object_or_404(Issue, pk=issue_id)
    if request.user != issue.issue_owner:
        return HttpResponseForbidden("You don't have permission to delete this issue.")
    issue.delete()
    return redirect('/')


@login_required(login_url="/login/")
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


@login_required(login_url="/login/")
def get_task(request, status_name, status_id):
    tasks = Task.objects.filter(status_id=status_id).select_related('project')
    context = {'tasks': tasks}
    return render(request, 'core/get_tasks.html', context)


@login_required(login_url="/login/")
def project_tasks(request, project_id):
    project = Project.objects.get(pk=project_id)
    task_statuses = TaskStatus.objects.all()
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


@login_required(login_url="/login/")
def all_tasks(request):
    tasks = (
        Task.objects
        .filter(assigned_to=request.user)
        .values('task_name', 'project__project_name', 'task_id')
    )
    context = {

        "tasks": tasks
    }
    return render(request, template_name="core/tasks.html", context=context)


@login_required(login_url="/login/")
def all_issues(request):
    issues = (  # need to change query
        Issue.objects
        .filter(assigned_to=request.user)
        .values('issue_name', 'project__project_name', 'issue_id')
    )
    context = {
        "issues": issues
    }
    return render(request, template_name="core/issues.html", context=context)


@login_required(login_url="/login/")
def create_project(request):
    if request.method == "POST":
        return HttpResponse("Submitted form")
    return render(request, template_name="core/create_project.html")


@login_required(login_url="/login/")
def create_task(request):
    if request.method == "POST":
        create_task_helper(request)
        return redirect('/')

    projects = Project.objects.filter(userproject__user=request.user)
    users = User.objects.all()

    context = {
        'projects': projects,
        'users': users,
    }
    return render(request, template_name="core/create_task.html", context=context)


def select_users(request):
    if request.method == 'GET' and 'project_id' in request.GET:
        project_id = request.GET['project_id']
        users = User.objects.filter(userproject__project_id=project_id)
        user_data = [{'id': user.id, 'username': user.username} for user in users]
        return JsonResponse(user_data, safe=False)
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required(login_url="/login/")
def create_issue(request):
    projects = Project.objects.all()
    users = User.objects.all()

    if create_issue_helper(request):
        return redirect('/')

    context = {
        'projects': projects,
        'users': users,
    }

    return render(request, template_name="core/create_issue.html", context=context)


@login_required(login_url="/login/")
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


@login_required(login_url="/login/")
def logout_user(request):
    logout(request)
    return redirect('/login/')
