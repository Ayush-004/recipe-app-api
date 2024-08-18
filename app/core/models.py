'''
Database models for custom user management.
'''
from django.db import models  # Importing Django's model base classes
from django.contrib.auth.models import (
    AbstractBaseUser,  # Provides core authentication functionality (e.g., password management)
    BaseUserManager,   # Base class for creating custom user managers
    PermissionsMixin,  # Adds fields and methods to support Django's permission framework
)

# Custom manager for handling user creation and management
class UserManager(BaseUserManager):
    '''Manager for users'''

    def create_user(self, email, password=None, **extra_fields):
        '''Create, save and return a new user.'''
        if not email:
            raise ValueError('User must have an email address.')
        # Normalize the email address by lowercasing the domain part
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)  # Hash the password before storing it
        user.save(using=self._db)  # Save the user to the database

        return user

    def create_superuser(self, email, password):
        '''Create and return a new superuser'''
        user = self.create_user(email, password)  # Create a regular user first
        user.is_staff = True  # Grant superuser privileges
        user.is_superuser = True
        user.save(using=self._db)  # Save the superuser to the database

        return user


# Custom user model replacing the default Django user model
class User(AbstractBaseUser, PermissionsMixin):
    '''User in the system.'''
    email = models.EmailField(max_length=255, unique=True)  # Email field, unique for each user
    name = models.CharField(max_length=255)  # Name field for storing the user's name
    is_active = models.BooleanField(default=True)  # Boolean field to track if the user is active
    is_staff = models.BooleanField(default=False)  # Boolean field to track if the user has admin access

    objects = UserManager()  # Assign the custom manager to handle user operations

    USERNAME_FIELD = 'email'  # Set email as the unique identifier for authentication

    # Additional fields and methods can be added here if needed