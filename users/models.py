from django.contrib.auth.models import AbstractUser
from django.contrib.sites.models import Site
from django.db import models

# Create your models here.


class Company(models.Model):
    name = models.CharField(max_length=255)
    site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class BlogUser(AbstractUser):
    company = models.ForeignKey(
        Company, on_delete=models.SET_NULL, null=True, blank=True
    )
