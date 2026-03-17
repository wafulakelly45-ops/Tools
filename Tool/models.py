from django.db import models

# Create your models here.

class Tool(models.Model):
    Name=models.CharField(max_length=50)
    cover=models.ImageField(upload_to="images/", null=True)
    Description=models.CharField(max_length=600)

    def __str__(self):
        return f"{self.id}:{self.Name} to {self.Description}"