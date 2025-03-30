from django.db import models

# Create your models here.

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField('criado em', auto_now_add=True, auto_now=False)
    modified_at = models.DateTimeField('modificado em', auto_now_add=True, auto_now=False)

    class Meta:
        abstract = True