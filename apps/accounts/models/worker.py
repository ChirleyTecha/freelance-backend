from django.db import models

class Worker(models.Model):
    user = models.OneToOneField('accounts.user', on_delete=models.CASCADE)
    skills = models.CharField(max_length=200)
    experience = models.CharField(max_length=200)

    def __str__(self):
        return self.user.username
