from django.db import models
from django.template.defaulttags import comment


class Jar(models.Model):
    monoid = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        verbose_name = 'Jar'
        verbose_name_plural = 'Jars'

    def __str__(self):
        return self.name
