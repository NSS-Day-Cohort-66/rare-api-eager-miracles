from django.db import models

class Reaction(models.Model):
    label = models.CharField(max_length=500, null=True, blank=True)
    image_url = models.CharField(max_length=500, null=True, blank=True)
    