from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from tms_auth.managers import AuthUserManager
from utils.enums import UserRole


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    extras = models.JSONField(default=dict)

    class Meta:
        abstract = True


class AuthUser(AbstractBaseUser, BaseModel):
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)
    user_number = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    passport = models.CharField(max_length=255, null=True, blank=True)
    role = models.CharField(max_length=255, choices=UserRole.choices(), default=UserRole.driver.value)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = AuthUserManager()

    class Meta:
        db_table = 'users'

    def has_perm(self, app_label):
        if self.is_active and self.is_superuser:
            return True
        return False

    def has_module_perms(self, app_label):
        if self.is_active and self.is_superuser:
            return True
        return False

    def get_full_name(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        return None
