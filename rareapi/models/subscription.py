from django.db import models

class Subscription(models.Model):
    author = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name='subscriptions_as_author')
    follower = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name='subscriptions_as_follower')
    created_on = models.DateField(auto_now_add=True)
    ended_on = models.DateField(null=True)
    
