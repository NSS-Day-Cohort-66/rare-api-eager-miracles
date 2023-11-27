from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts_by_author')
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name='this_category_posts')
    title = models.CharField(max_length=500, null=True, blank=True)
    pub_date = models.DateField(auto_now_add=True)
    image_url = models.URLField(max_length=500, null=True, blank=True)
    content = models.CharField(max_length=500, null=True, blank=True)
    approved = models.BooleanField(default=True)
    reactions = models.ManyToManyField(
        "Reaction",
        through='PostReaction',
        related_name="reactions"
    )
    tags = models.ManyToManyField(
        "Tag",
        through='PostTag',
        related_name="tags"
    )
