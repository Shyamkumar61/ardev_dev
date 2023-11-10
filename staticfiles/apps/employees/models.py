from django.db import models
from django_extensions.db.models import TimeStampedModel
from apps.general.models import Designation
from django.core.exceptions import ValidationError

# Create your models here.


def check_value(value):
    if value is None:
        raise ValueError("No Numbers are Allowed")
    return value


class Employee(TimeStampedModel):

    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'

    APositive = 'A+'
    ANegative = 'A-'
    BPositive = 'B+'
    BNegative = 'B-'
    ABPositive = 'AB+'
    ABNegative = 'AB-'
    OPositive = 'O+'
    ONegative = 'O-'

    GENDER_CHOICE = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other')
    )

    BloodGroupChoice = (
        (APositive, 'A+'),
        (ANegative, 'A-'),
        (BPositive, 'B+'),
        (BNegative, 'B-'),
        (ABPositive, 'AB+'),
        (ABNegative, 'AB-'),
        (OPositive, 'O+'),
        (ONegative, 'O-')
    )

    emp_id = models.CharField(max_length=20, primary_key=True, unique=True)
    name = models.CharField(max_length=30)
    phone_no = models.CharField(max_length=15, unique=True)
    whatsappNum = models.CharField(max_length=15)
    email = models.CharField(max_length=30, blank=True, null=True)
    address = models.TextField()
    gender = models.CharField(choices=GENDER_CHOICE, max_length=10)
    bloodGroup = models.CharField(choices=BloodGroupChoice, max_length=5)
    uanNumber = models.CharField(max_length=20, unique=True)
    aadhar = models.CharField(max_length=20, unique=True)
    pan_card = models.CharField(max_length=30, blank=True, null=True)
    esiNumber = models.CharField(max_length=30, blank=True, null=True)
    dob = models.DateTimeField()
    designation = models.ForeignKey(Designation, on_delete=models.SET_NULL, related_name='employee')
    profile_img = models.ImageField(blank=True, upload_to='images/user_profile/')
    pcc_image = models.ImageField(blank=True, upload_to='images/emp_pcc/')
    aadhar_image = models.ImageField(blank=True, upload_to='images/emp_aadhar/')
    bank_passbook = models.ImageField(blank=True, upload_to='images/emp_passbook')

    class Meta:
        verbose_name = 'Employees'
        verbose_name_plural = 'Employess'
        indexes = (models.Index(fields=['phone_no', 'aadhar', 'esiNumber']))

    def get_employee_age(self):
        pass



