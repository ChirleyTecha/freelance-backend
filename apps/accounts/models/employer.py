from django.db import models

class Employer(models.Model):
    user = models.OneToOneField('accounts.user', on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    address = models.CharField(max_length=150)

    def __str__(self):
        return self.company_name