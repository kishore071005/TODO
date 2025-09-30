from django.urls import path
from . import views

urlpatterns = [
    # Authentication URLs
    path('', views.login_view, name='login'),                       # Login page (homepage)
    path('register/', views.register_view, name='register'),        # Register page
    path('logout/', views.logout_view, name='logout'),              # Logout
    
    # Task URLs (require login)
    path('tasks/', views.task_list, name='task_list'),              # Task list page
    path('tasks/add/', views.add_task, name='add_task'),            # Add new task page
    path('tasks/delete/<int:task_id>/', views.delete_task, name='delete_task'),  # Delete task
]