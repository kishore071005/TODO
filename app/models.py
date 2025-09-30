from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    """Simple model for TODO tasks - add and delete only"""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')  # Link to user
    
    class Meta:
        ordering = ['-created_at']  # Show newest tasks first
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"