from django.db import models


class Worker(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE)
    skills = models.CharField(max_length=200)
    experience = models.CharField(max_length=200)

    class Meta:
        db_table = 'workers'

    def __str__(self):
        return self.user.username
