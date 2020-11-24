from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.base_user import BaseUserManager

class MyOwnerManager(BaseUserManager):

# Function used for creating/modifying new owners


    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('Owners must have a username')

        user = self.model(
            username = username,
            email = email,
            password = password,
            **extra_fields
        )

        # Defines what the owner model will consist of

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_owner(self, username, email, password, **extra_fields):
        return self._create_user(username, email, password, **extra_fields)

    def edit_owner(self, instance, username, email):
        # We edit the owner instance by overwriting it with
        # Validated request data
        instance.username = username.value
        instance.email = email.value
        instance.save()
        return instance

class Owner(User):

# We are inheriting fom Django's base User model because
# djangorestframework's authentication is based around it
# Can be completely custom, but would have to create
# custom authentication as well

    objects = MyOwnerManager()

# Inherits the properties of the above manager
# in charge of creating/editing

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
