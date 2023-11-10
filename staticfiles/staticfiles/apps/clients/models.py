from django.db import models
from django_extensions.db.models import TimeStampedModel
from apps.general.models import Services, Designation

# Create your models here.


class Client(TimeStampedModel):

    STATE_GOVT = 'state_govt'
    CENTRAL_GOVT = 'central_govt'
    PRIVATE = 'private'

    SECTOR_CHOICES = (
        (STATE_GOVT, 'State Govt'),
        (CENTRAL_GOVT, 'Central Govt'),
        (PRIVATE, 'Private'),
    )

    SHIFT_ONE = 'shift_one'
    SHIFT_TWO = 'shift_two'
    SHIFT_THREE = 'shift_three'

    SHIFT_CHOICES = (
        (SHIFT_ONE, 'One Shift'),
        (SHIFT_TWO, 'Two Shift'),
        (SHIFT_THREE, 'Three Shift')
    )

    client_name = models.CharField(max_length=50)
    sector = models.CharField(choices=SECTOR_CHOICES, max_length=20)
    client_gst = models.CharField(max_length=255, blank=True, null=True)
    contract_singed = models.DateField(blank=True, null=True)
    contract_period = models.DateTimeField()
    client_email = models.EmailField(null=True, blank=True)
    client_phone = models.CharField(max_length=20, null=True, blank=True)
    client_address = models.TextField()
    client_city = models.CharField(max_length=50, blank=True, null=True)
    client_pincode = models.CharField(max_length=50, blank=True, null=True)
    service = models.ManyToManyField(Services, blank=True, related_name='client_service')
    designation = models.ManyToManyField(Designation, blank=True, related_name='client_designation')
    active_status = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Client'

