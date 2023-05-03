from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator, MinLengthValidator
from django.db import models
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(_('username'), max_length=255, validators=[MinLengthValidator(4)])
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)
    password = models.CharField(max_length=128, validators=[MinLengthValidator(8)])
    password2 = models.CharField(max_length=128, validators=[MinLengthValidator(8)], default='')
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+01111111111'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(_('phone number'), validators=[phone_regex], max_length=17, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name', 'last_name', 'password', 'password2', 'phone_number']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def clean(self):
        super().clean()
        errors = {}
        if not self.phone_number:
            errors['phone_number'] = _('Phone number is required.')
        if errors:
            raise ValidationError(errors)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')