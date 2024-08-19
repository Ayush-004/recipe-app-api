"""
Views for the recipe APIs
"""
from rest_framework import viewsets  # Importing viewsets from Django REST Framework, which provide CRUD operations
from rest_framework.authentication import TokenAuthentication  # Importing TokenAuthentication for securing API endpoints
from rest_framework.permissions import IsAuthenticated  # Importing IsAuthenticated to restrict access to authenticated users

from core.models import Recipe  # Importing the Recipe model from the core app
from recipe import serializers  # Importing the serializers module from the recipe app


class RecipeViewSet(viewsets.ModelViewSet):
    """View for managing recipe APIs."""

    # Specify the default serializer class that should be used for this viewset
    serializer_class = serializers.RecipeDetailSerializer # RecipeDetailSerializer is used for detailed views to access description as well

    # Define the queryset that this viewset will operate on
    queryset = Recipe.objects.all()

    # Specify the authentication classes that will be used to authenticate users
    authentication_classes = [TokenAuthentication]

    # Specify the permission classes that will be used to restrict access to authenticated users only
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve recipes for the authenticated user."""
        # Override the default queryset to filter recipes by the authenticated user
        # This ensures that users only see their own recipes
        return self.queryset.filter(user=self.request.user).order_by('-id')
        # The queryset is ordered by 'id' in descending order to show the most recent recipes first

    #expects a reference to a class
    def get_serializer_class(self): # Helps to determine the class that is being used to serialize and deserialze the data
        """Return the appropriate serializer class for the request."""
        # If the action is 'list', use the RecipeSerializer to return a simplified representation of the recipes
        if self.action == 'list':
            return serializers.RecipeSerializer

        # Otherwise, use the default serializer class (RecipeDetailSerializer) for detailed views
        return self.serializer_class

    def perform_create(self, serializer): # This is a function that is called when we create an object
        
        """Create a new recipe."""
        serializer.save(user=self.request.user) # Assign the authenticated user to the recipe being created