from autoslug import AutoSlugField
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils import timezone

from digisign import settings
from digisign.access_groups.models import AccessGroup


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


def get_username(instance):
    """ Used for auto-slug functionality -- returns the username portion of
    the user's specified email address.
    """
    return instance.email.split('@')[0]


class User(AbstractUser):
    class UserType(models.TextChoices):
        regular = 'regular', 'Regular'
        lecturer = 'lecturer', 'Lecturer'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    username = AutoSlugField(populate_from=get_username, blank=True, unique=True)
    email = models.EmailField('email address', unique=True)
    first_name = models.CharField('first name', max_length=150, blank=True)
    birth_date = models.DateField('birth date', blank=True, null=True)
    phone_number = models.CharField(
        'phone number',
        max_length=25,
        blank=True,
        null=True,
        unique=True
    )
    user_type = models.CharField(
        choices=UserType.choices,
        max_length=30,
        default=UserType.regular
    )
    access_group = models.ForeignKey(
        AccessGroup,
        related_name='users',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name='access group'
    )
    deleted = models.DateTimeField(
        'deleted',
        blank=True,
        null=True,
        help_text='Date/time this object was deleted.'
    )
    objects = CustomUserManager()

    class Meta:
        db_table = 'auth_user'
        ordering = ('date_joined',)

    @property
    def is_deleted(self):
        return True if self.deleted else False

    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.deleted = timezone.now()
        self.save()


class Profile(models.Model):
    """ Additional user profile data.
    """
    class Gender(models.TextChoices):
        MALE = 'male', 'Male'
        FEMALE = 'female', 'Female'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='profile',
        on_delete=models.CASCADE
    )
    gender = models.CharField(
        'gender',
        max_length=50,
        choices=Gender.choices,
        blank=True
    )
    address = models.CharField('address', max_length=255, blank=True)

    class Meta:
        db_table = 'auth_user_profile'
