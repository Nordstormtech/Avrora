from django.db import models


class People(models.Model):
    name = models.CharField(max_length=100)
    level = models.TextField()
    number = models.CharField(max_length=40)

    def __str__(self):
        return self.number
