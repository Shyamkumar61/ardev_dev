from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import AccountManager
from django.core.exceptions import ValidationError
from django.utils import timezone
# Create your models here.


def validate_name(value):
    if value and not value.isalpha():
        raise ValidationError("No Numbers are Allowed")
    return value


class Account(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_("Email Field"), unique=True, max_length=30)
    username = models.CharField(_("username"), unique=True, max_length=20)
    first_name = models.CharField(_("first name"), max_length=20, validators=[validate_name])
    last_name = models.CharField(_("last_name"), max_length=20, validators=[validate_name])
    image = models.ImageField(blank=True, null=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting account."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = AccountManager()

    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Account'

    def get_full_name(self):
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name

