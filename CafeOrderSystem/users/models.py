from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, password, **extra_fields):

        username = extra_fields.get('username')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Список пользователей'
        ordering = ['username']
        indexes = [
            models.Index(fields=['username'])
        ]

    REQUIRED_FIELDS = []
    objects = UserManager()
    USERNAME_FIELD = 'username'
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=200,
        help_text=_('Required. 200 characters or fewer.\
                     Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _('A user with that username already exists.'),
        },
        unique=True
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts. '
        ),
    )

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'


