from django.db import models

class Document(models.Model):


    employer = models.OneToOneField('accounts.Employer', on_delete=models.CASCADE)

    document_type = models.CharField(max_length=100)
    file_path = models.CharField(max_length=255)

    is_validated = models.BooleanField(default=False)
    date_uploaded = models.DateTimeField(auto_now_add=True)

    def validate(self):
        
        self.is_validated = True
        self.save()

    def __str__(self):
        return f"Document - {self.document_type}"