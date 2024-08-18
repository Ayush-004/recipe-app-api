"""
Views for the user API.
"""
from rest_framework import generics  # Importing generic views from Django REST Framework (DRF)

from user.serializers import UserSerializer  # Importing the custom serializer for the User model


# Define a view to handle the creation of new users
class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""

    # Specify the serializer class that should be used for this view
    serializer_class = UserSerializer