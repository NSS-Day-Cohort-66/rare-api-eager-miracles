from django.db import models

class DemotionQueue(models.Model):
    admin = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name='demotions_as_admin')
    approver_one = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name='demotions_as_approver')
    action = models.CharField(max_length=500, null=True, blank=True)
    
