"""
Serializers for the user API View.
"""
from django.contrib.auth import (  # Importing the authentication functions from Django
    get_user_model,  # Importing the get_user_model function to retrieve the current user model
    authenticate,  # Importing the authenticate function to verify user credentials
)
from django.utils.translation import gettext as _  # Importing the gettext function for handling translations
from rest_framework import serializers  # Importing the serializers module from Django REST Framework

# Define a serializer for the User model, which will handle serialization and deserialization of user data
class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        """Meta class to define the serializer behavior and fields."""
        model = get_user_model()  # Specifies that this serializer should use the current user model
        fields = ['email', 'password', 'name']  # Specifies the fields that will be included in the serialization
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}
        # extra_kwargs:
        # - 'password': {'write_only': True} ensures the password field is only used for input and not output,
        #               so it won't be exposed in API responses.
        # - 'min_length': 5 ensures that passwords must be at least 5 characters long.

    # Override the create method to handle the creation of a new user with a hashed password
    def create(self, validated_data):
        """Create and return a user with an encrypted password."""
        # The create_user method ensures that the password is hashed before saving the user
        return get_user_model().objects.create_user(**validated_data)
        # **validated_data unpacks the validated data dictionary into keyword arguments for create_user

    # Override the update method to handle updating the user, including password handling
    def update(self, instance, validated_data):
        """Update and return user."""
        # Extract the password from the validated data, if provided, and remove it from the dictionary
        password = validated_data.pop('password', None)

        # Call the superclass's update method to update the user instance with the remaining validated data
        user = super().update(instance, validated_data)

        # If a password was provided, hash it and save the updated user object
        if password:
            user.set_password(password)  # Hash the password
            user.save()  # Save the user with the updated password

        # Return the updated user object
        return user



# Define a serializer for generating authentication tokens for users
class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication token."""

    # Define fields for email and password, with specific styling and behavior
    email = serializers.EmailField()  # Email field for entering the user's email address
    password = serializers.CharField(
        style={'input_type': 'password'},  # Ensures that the input field renders as a password input in forms
        trim_whitespace=False,  # Ensures that leading and trailing whitespaces are not trimmed from the password
    )

    # Override the validate method to include custom validation logic
    def validate(self, attrs):
        """Validate and authenticate the user."""

        # Extract email and password from the validated data
        email = attrs.get('email')
        password = attrs.get('password')

        # Authenticate the user using the provided credentials
        user = authenticate(
            request=self.context.get('request'),  # Pass the request context if available
            username=email,  # Use the email as the username for authentication
            password=password,  # Use the provided password for authentication
        )

        # If the user is not authenticated, raise a validation error
        if not user:
            msg = _('Unable to authenticate with provided credentials.')  # Error message for failed authentication
            raise serializers.ValidationError(msg, code='authorization')  # Raise an exception with the error message

        # If authentication is successful, add the user to the validated data and set user to the view
        attrs['user'] = user
        return attrs  # Return the validated data with the authenticated user