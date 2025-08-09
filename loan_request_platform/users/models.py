from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=255)
    email_address = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.name} <{self.email_address}>"