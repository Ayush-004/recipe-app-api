'''
Database models for custom user management.
'''
from django.db import models  # Importing Django's model base classes
from django.contrib.auth.models import (
    AbstractBaseUser,  # Provides core authentication functionality (e.g., password management)
    BaseUserManager,   # Base class for creating custom user managers
    PermissionsMixin,  # Adds fields and methods to support Django's permission framework
)
from django.conf import settings # Importing Django's settings module

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

#Recipe based on models.model of django, different from our user as the user class mei we were extending the base user model
class Recipe(models.Model):
    """Recipe object."""

    # ForeignKey relationship to the User model
    # This links each recipe to a specific user, ensuring that each recipe is owned by a user.
    # settings.AUTH_USER_MODEL refers to the custom user model defined in the project settings.
    # on_delete=models.CASCADE ensures that if a user is deleted, all their associated recipes are also deleted.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    # CharField for the title of the recipe with a maximum length of 255 characters
    title = models.CharField(max_length=255)

    # TextField for the description of the recipe.
    # blank=True allows the description to be optional (i.e., can be left empty).
    description = models.TextField(blank=True)

    # IntegerField to store the time required to prepare the recipe, in minutes
    time_minutes = models.IntegerField()

    # DecimalField to store the price of the recipe
    # max_digits=5 allows for a price up to 999.99
    # decimal_places=2 ensures that the price is stored with two decimal places
    price = models.DecimalField(max_digits=5, decimal_places=2)

    # CharField for an optional link to the recipe (e.g., a URL for an online recipe)
    # blank=True allows this field to be optional
    link = models.CharField(max_length=255, blank=True)

    # The __str__ method returns the title of the recipe as its string representation
    # This is useful for displaying the recipe in admin interfaces or when printing the object.
    def __str__(self):
        return self.title