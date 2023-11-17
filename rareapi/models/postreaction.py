from django.db import models

class PostReaction(models.Model):
    user = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name='rare_users')
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name='reactions_on_this_post')
    reaction = models.ForeignKey("Reaction", on_delete=models.CASCADE, related_name='posts_with_this_reaction')
    