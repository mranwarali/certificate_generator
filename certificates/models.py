from django.db import models

class Certificate(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField()
    issue_date = models.DateField()
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.name
