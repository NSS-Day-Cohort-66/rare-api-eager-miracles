from django.db import models

class Comment(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name='post_comments')
    author = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name='user_comments')
    created_on = models.DateField(auto_now_add=True)
    content = models.CharField(max_length=500, null=True, blank=True)
    subject = models.CharField(max_length=50, null=True, blank=True)