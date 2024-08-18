"""
Serializers for the user API View.
"""
from django.contrib.auth import get_user_model  # Importing the function to get the user model in use
from rest_framework import serializers  # Importing the serializers module from Django REST Framework

# Define a serializer for the User model, which will handle serialization and deserialization of user data
class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        """Meta class to define the serializer behavior and fields."""
        model = get_user_model()  # Specifies that this serializer should use the current user model
        fields = ['email', 'password', 'name']  # Specifies the fields that will be included in the serialization, things saved in model.
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}
        # extra_kwargs:
        # - 'password': {'write_only': True} ensures the password field is only used for input and not output,
        #               so it won't be exposed in API responses.
        # - 'min_length': 5 ensures that passwords must be at least 5 characters long.

    # Override the create method to handle the creation of a new user with a hashed password
    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        # The create_user method ensures that the password is hashed before saving the user, this method is called after the validation
        return get_user_model().objects.create_user(**validated_data)
        # **validated_data unpacks the validated data dictionary into keyword arguments for create_user