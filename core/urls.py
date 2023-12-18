from django.contrib import admin
from django.urls import path, include
from core.views import (
    login, home, view_task, user_projects, get_task, project_tasks, view_issue,
    all_tasks, all_issues, create_project, create_issue, create_task, complete_profile,
    add_developer
    )
urlpatterns = [
    # path("login/", Login.as_view(), name="login"),
    path("login/", login, name="login"),
    path("", home, name="home"),
    path('view_task/<int:task_id>/', view_task, name='view_task'),
    path('view_issue/<int:issue_id>/', view_issue, name='view_issue'),
    path('projects/', user_projects, name='user_projects'),
    path('tasks/<str:status_name>/<int:status_id>', get_task, name='get_task'),
    path('project/<int:project_id>/tasks', project_tasks, name='project_tasks'),
    path('tasks/', all_tasks, name="all_tasks"),
    path('issues/', all_issues, name="all_issues"),
    path('create-project/', create_project, name='create_project'),
    path('add_developer/', add_developer, name='add_developer'),
    path('create-task/', create_task, name='create_task'),
    path('create-issue/', create_issue, name='create_issue'),
    path('complete-profile/', complete_profile, name='complete_profile'),
]