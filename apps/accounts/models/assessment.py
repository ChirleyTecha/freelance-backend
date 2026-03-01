from django.db import models


class Assessment(models.Model):
    # id is automatically created by Django (Integer, Primary Key)

    worker = models.OneToOneField('accounts.Worker', on_delete=models.CASCADE)

    score = models.IntegerField()
    comment = models.CharField(max_length=255)

    is_approved = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def register(self):
        """
        This method registers the assessment.
        If score is 50 or more, the freelancer is approved.
        """

        if self.score >= 50:
            self.is_approved = True
        else:
            self.is_approved = False

        self.save()

    def __str__(self):
        return f"Assessment - {self.worker.user.username}"