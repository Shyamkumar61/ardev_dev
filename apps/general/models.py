from django.db import models
from django_extensions.db.models import TimeStampedModel
from autoslug import AutoSlugField
# Create your models here.


class Services(TimeStampedModel):

    service_name = models.CharField(max_length=50)
    slug = AutoSlugField(max_length=20, populate_from='service_name')

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Service'


class Designation(TimeStampedModel):

    service = models.ForeignKey(Services, on_delete=models.CASCADE, related_name='designations')
    name = models.CharField(max_length=50)
    slug = AutoSlugField(max_length=50, populate_from='name')

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Service'


