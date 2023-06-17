from django.db import models


class Jar(models.Model):
    monoJarid = models.CharField(max_length=255, unique=True)
    monoid = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        verbose_name = 'Jar'
        verbose_name_plural = 'Jars'

    def __str__(self):
        return self.name
