from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class RareUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rare_users')
    bio = models.CharField(max_length=500, null=True, blank=True)
    image_url = models.URLField(max_length=155, null=True, blank=True)
    created_on = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)
