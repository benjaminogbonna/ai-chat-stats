from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser

from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField(_("username"), max_length=150, unique=True)
    name = models.CharField(_("name"), max_length=150, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    # date_joined = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=120, default='', unique=True)
    data = models.FileField(upload_to='data/', default='', null=True, max_length=500)
    total_convs = models.IntegerField(default=0, null=True, blank=True)


    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    class Meta:
        ordering = ('-date_joined',)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('main:view_user_profile',
                       kwargs={
                           'slug': self.slug,
                       })


    def save(self, *args, **kwargs):
        self.slug = self.username
        if self.pk:
            existing_file = User.objects.filter(pk=self.pk).first()
            if existing_file and existing_file.data != self.data:
                if existing_file.data:
                    existing_file.data.delete(save=False)
        super().save(*args, **kwargs)

