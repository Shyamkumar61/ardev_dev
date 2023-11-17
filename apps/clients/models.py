from django.db import models
from django_extensions.db.models import TimeStampedModel
from apps.general.models import Services, Designation

# Create your models here.


class Client(TimeStampedModel):

    STATE_GOVT = 'state_govt'
    CENTRAL_GOVT = 'central_govt'
    PRIVATE = 'private'

    DAY_SHIFT = 'day_shift'
    NIGHT_SHIFT = 'night_shift'
    ROUND_SHIFT = 'round_shift'

    SQ_FEET = 'sq_feet'
    MAN_POWER = 'man_power'

    SECTOR_CHOICES = (
        (STATE_GOVT, 'State Govt'),
        (CENTRAL_GOVT, 'Central Govt'),
        (PRIVATE, 'Private'),
    )

    SHIFT_CHOICES = (
        (DAY_SHIFT, 'Day Shift'),
        (NIGHT_SHIFT, 'Night Shift'),
        (ROUND_SHIFT, 'Round Shift')
    )

    BILLING_CHOICES = (
        (SQ_FEET, 'Sq Feet'),
        (MAN_POWER, 'Man Power')
    )

    client_name = models.CharField(max_length=50)
    sector = models.CharField(choices=SECTOR_CHOICES, max_length=20)
    client_gst = models.CharField(max_length=255, blank=True, null=True)
    contract_singed = models.DateField(blank=True, null=True)
    contract_period = models.DateField(blank=True, null=True)
    client_email = models.EmailField(null=True, blank=True)
    client_phone = models.CharField(max_length=20, null=True, blank=True)
    client_address = models.TextField(null=True, blank=True)
    client_city = models.CharField(max_length=50, blank=True, null=True)
    client_pincode = models.CharField(max_length=50, blank=True, null=True)
    service = models.ManyToManyField(Services, blank=True, related_name='client_services')
    designation = models.ManyToManyField(Designation, blank=True, related_name='client_designations')
    lut_tenure = models.CharField(max_length=50)
    bid_amount = models.DecimalField(max_digits=20, decimal_places=2)
    billing_type = models.CharField(choices=BILLING_CHOICES, max_length=20)
    client_logo = models.ImageField(upload_to='client_logos', default='default_logo.jpg')
    active_status = models.BooleanField(default=True)

    objects = models.Manager()

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Client'

    def __str__(self):
        return self.client_name
