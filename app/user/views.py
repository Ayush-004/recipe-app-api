"""
Views for the user API.
"""
from rest_framework import generics, authentication, permissions  # Importing necessary modules from Django REST Framework (DRF)
from rest_framework.authtoken.views import ObtainAuthToken  # Importing the ObtainAuthToken view for handling token authentication
from rest_framework.settings import api_settings  # Importing API settings to customize view behavior, such as rendering

from user.serializers import (  # Importing the serializers that handle data validation and serialization
    UserSerializer,  # Serializer for creating and managing user data
    AuthTokenSerializer,  # Serializer for handling user authentication and token generation
)

# Define a view to handle the creation of new users
class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""

    # Specify the serializer class that should be used for this view
    serializer_class = UserSerializer
    # The CreateAPIView automatically provides the `POST` method to create a new user using the specified serializer


# Define a view to handle the creation of auth tokens for users
class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""

    # Specify the serializer class that should be used for this view
    serializer_class = AuthTokenSerializer
    # ObtainAuthToken typically uses username and password for authentication.
    # We override it to use email and password instead, by specifying our custom AuthTokenSerializer.

    # Specify the renderer classes to use for this view, which control how the response is rendered
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    # This allows the view to use the default renderer classes specified in the API settings,
    # enabling the browsable API feature, which provides a user-friendly interface for testing the API.

# Define a view to handle retrieval and updating of the authenticated user's data
class ManageUserView(generics.RetrieveUpdateAPIView): #Retreive is HTTP get, Update is HTTP put, patch
    # Must be authenticated to use this API
    """Manage the authenticated user."""

    # Specify the serializer class to be used for this view
    serializer_class = UserSerializer
    # This serializer will handle the serialization and deserialization of user data for this view.

    # Specify the authentication classes to be used for this view
    authentication_classes = [authentication.TokenAuthentication]
    # TokenAuthentication ensures that the user is authenticated via token before they can access this view.

    # Specify the permission classes to be used for this view
    permission_classes = [permissions.IsAuthenticated]
    # IsAuthenticated ensures that only authenticated users can access this view.

    def get_object(self):
        """Retrieve and return the authenticated user."""
        # Override the get_object method to return the current authenticated user
        return self.request.user
        # This method is called when the view is accessed to retrieve the user's data
        # Since this view is for managing the authenticated user's profile, we return self.request.user.