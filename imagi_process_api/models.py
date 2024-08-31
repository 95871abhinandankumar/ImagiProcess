# models.py

from django.db import models

class RequestStatus(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'Waiting'),
        ('inProgress', 'In Progress'),
        ('completed', 'Completed'),
        ('error', 'Error'),
    ]
    
    request_id = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='waiting')
    result = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)