from django.contrib import admin
from .models import User, UserTechnology, UserRole, Project, UserProject, UserTask, Task, TaskStatus, UserDetail, Issue, IssueStatus
from django.contrib.auth.admin import UserAdmin

# Register your models her
# e.

@admin.register(UserDetail)
class UserDetailAdmin(admin.ModelAdmin):
    list_display = ('user',)

@admin.register(UserTechnology)
class UserTechnologyAdmin(admin.ModelAdmin):
    list_display = ('technology_name',)

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('role_name',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'created_at', 'updated_at', 'created_by')

@admin.register(UserProject)
class UserProjectAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'joined_at')

@admin.register(UserTask)
class UserTaskAdmin(admin.ModelAdmin):
    list_display = ('user', 'task')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_name', 'project', 'assigned_to', 'status', 'task_owner', 'created_at', 'updated_at')

@admin.register(TaskStatus)
class TaskStatusAdmin(admin.ModelAdmin):
    list_display = ('status_name',)

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ['issue_id', 'issue_name', 'project', 'assigned_to', 'status', 'created_at']
    search_fields = ['issue_name', 'task_description']
    list_filter = ['status', 'created_at']
    date_hierarchy = 'created_at'

@admin.register(IssueStatus)
class IssueStatusAdmin(admin.ModelAdmin):
    list_display = ['status_id', 'status_name']