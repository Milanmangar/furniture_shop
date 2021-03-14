from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Feet(models.Model):
    name = models.CharField(primary_key=True, max_length=255)
    width = models.IntegerField(default=0, blank=True, null=True)
    length = models.IntegerField(default=0, blank=True, null=True)
    radius = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return self.name


class Leg(models.Model):
    name = models.CharField(primary_key=True, max_length=255)
    foldable = models.BooleanField(default=False)
    feet = models.ForeignKey(Feet, related_name="feet", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Table(models.Model):
    name = models.CharField(primary_key=True, max_length=255)
    legs = models.OneToOneField(Leg, null=True, blank=True, on_delete=models.CASCADE)
    description = models.TextField(default="", blank=True, null=True)
    price = models.IntegerField(default=0, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_date"]

    def __str__(self):
        return self.name
