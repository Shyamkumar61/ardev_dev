from django.db import models
from django_extensions.db.models import TimeStampedModel
from apps.general.models import Designation
from apps.clients.models import Client
from apps.general.models import Banks
from PIL import Image as PILImage
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
    phone_no = models.CharField(max_length=15, unique=True, db_index=True)
    whatsappNum = models.CharField(max_length=15, blank=True, null=True)
    email = models.CharField(max_length=30, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    gender = models.CharField(choices=GENDER_CHOICE, max_length=10)
    bloodGroup = models.CharField(choices=BloodGroupChoice, max_length=5, blank=True, null=True)
    uanNumber = models.CharField(max_length=20, null=True, blank=True, unique=True)
    aadhar = models.CharField(max_length=20, unique=True)
    pan_card = models.CharField(max_length=30, blank=True, null=True)
    esiNumber = models.CharField(max_length=30, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE, related_name='employee', blank=True,
                                    null=True)
    current_company = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='employee_company', blank=True,
                                        null=True)
    joining_date = models.DateField()
    profile_img = models.ImageField(blank=True, null=True, upload_to='user_profile/')
    pcc_image = models.ImageField(blank=True, null=True, upload_to='emp_pcc/')
    aadhar_image = models.ImageField(blank=True, null=True, upload_to='emp_aadhar/')
    bank_passbook = models.ImageField(blank=True, null=True, upload_to='emp_passbook/')
    is_active = models.BooleanField(default=True)
    objects = models.Manager

    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employee'
        indexes = (
            models.Index(
                fields=('phone_no', 'aadhar', 'esiNumber')
                ),
            )

    def __str__(self):
        return self.name

    def image_format(self, attrs):
        if attrs is not None:
            image = PILImage.open(attrs)
            image_fmt = image.format.lower()
            return image_fmt

    @property
    def get_pcc_image(self):
        if self.pcc_image:
            return True
        return False

    @property
    def get_aadhar_image(self):
        if self.aadhar_image:
            return True
        return False

    @property
    def get_doc(self):
        doc_list = list
        if self.pcc_image:
            doc_list.append(self.pcc_image)
        if self.aadhar_image:
            doc_list.append(self.pcc_image)
        return doc_list


class EmployeeBank(TimeStampedModel):
    bank = models.ForeignKey(Banks, on_delete=models.CASCADE, related_name='employee_bank')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='emp_bank')
    accountNumber = models.CharField(max_length=20, unique=True)
    ifscCode = models.CharField(max_length=20)

    objects = models.Manager()

    class Meta:
        verbose_name = 'Employee Bank'
        verbose_name_plural = 'Employee Bank'

    def __str__(self):
        return self.employee.name


class EmployeeHistory(TimeStampedModel):

    emp_id = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name="emp_history")
    prev_company = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name="worked_company")
    joined_date = models.DateField(blank=True, null=True)
    last_worked = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()

    def __str__(self):
        return f"{self.emp_id} - {self.prev_company}"

    class Meta:
        verbose_name = 'Employee History'
        verbose_name_plural = 'Employee History'

    def save(self, **kwargs):
        self.prev_company = self.emp_id.current_company
        super().save(**kwargs)

    def save_history(self, emp_id, prev_company, joined_date, last_worked):
        self.emp_id = emp_id
        self.prev_company = prev_company
        self.joined_date = joined_date
        self.last_worked = last_worked
        self.is_active = True
        self.save()


class ShiftEmployee(TimeStampedModel):

    emp_id = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name="shift_emp")
    prev_company = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name="prev_company")
    shifted_company = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True,
                                        related_name="current_company")
    from_date = models.DateField()
    to_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.emp_id} - {self.prev_company}"

    class Meta:
        verbose_name = 'Shifted Employee'
        verbose_name_plural = 'Shifted Employee'

    def save(self, **kwargs):
        self.prev_company = self.emp_id.current_company
        return super().save(**kwargs)
    
    def save_temporary(self, **kwargs):
        return super().save(**kwargs)