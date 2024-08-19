"""
Serializers for recipe APIs
"""
from rest_framework import serializers  # Importing the serializers module from Django REST Framework

from core.models import Recipe  # Importing the Recipe model from the core app


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes."""

    # The Meta class is used to define the model to serialize and the fields to include
    class Meta:
        model = Recipe  # Specifies that this serializer is for the Recipe model
        fields = ['id', 'title', 'time_minutes', 'price', 'link']  # Lists the fields to include in the serialized output
        read_only_fields = ['id']  # Specifies that the 'id' field should be read-only, meaning it cannot be modified through the serializer

class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail view."""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']  # Extends the fields from RecipeSerializer to include the 'description' field