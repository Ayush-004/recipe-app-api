"""
Tests for recipe APIs.
"""
from decimal import Decimal  # Importing Decimal for precise handling of currency or fixed-point arithmetic

from django.contrib.auth import get_user_model  # Importing function to get the user model
from django.test import TestCase  # Importing Django's test case class for creating unit tests
from django.urls import reverse  # Importing reverse function to dynamically generate URLs

from rest_framework import status  # Importing status codes for API responses
from rest_framework.test import APIClient  # Importing APIClient to simulate API requests

from core.models import Recipe  # Importing the Recipe model from the core app

from recipe.serializers import(
    RecipeSerializer,  # Importing RecipeSerializer for serializing Recipe objects
    RecipeDetailSerializer, # Importing RecipeDetailSerializer for serializing Recipe objects with details
)

# Define a URL for accessing the list of recipes in the API
RECIPES_URL = reverse('recipe:recipe-list')

def detail_url(recipe_id):
    """Create and return a recipe detail URL."""
    # Reverse function is used to generate the specific URL for a recipe's detail view, given its ID
    return reverse('recipe:recipe-detail', args=[recipe_id])

def create_recipe(user, **params):
    """Create and return a sample recipe."""
    # Default parameters for creating a sample recipe
    defaults = {
        'title': 'Sample recipe title',
        'time_minutes': 22,
        'price': Decimal('5.25'),
        'description': 'Sample description',
        'link': 'http://example.com/recipe.pdf',
    }
    # Update default parameters with any additional parameters provided
    defaults.update(params)

    # Create a new Recipe object with the user and the specified parameters
    recipe = Recipe.objects.create(user=user, **defaults)
    return recipe

class PublicRecipeAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        # Set up an API client to be used for the tests
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        # Make a GET request to the recipe list URL without authentication
        res = self.client.get(RECIPES_URL)

        # Assert that the request fails with a 401 Unauthorized status code
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateRecipeApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        # Set up an API client and a user to authenticate the client
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123',
        )
        # Force authentication for the API client with the created user
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """Test retrieving a list of recipes."""
        # Create two sample recipes for the authenticated user
        create_recipe(user=self.user)
        create_recipe(user=self.user)

        # Make a GET request to retrieve the list of recipes
        res = self.client.get(RECIPES_URL)

        # Retrieve all Recipe objects from the database, ordered by descending ID
        recipes = Recipe.objects.all().order_by('-id')
        # Serialize the Recipe objects to JSON format
        serializer = RecipeSerializer(recipes, many=True)  # many=True indicates we're serializing a list of items
        # Assert that the request was successful with a 200 OK status code
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # Assert that the response data matches the serialized Recipe data
        self.assertEqual(res.data, serializer.data)

    def test_recipe_list_limited_to_user(self):
        """Test list of recipes is limited to authenticated user."""
        # Create a sample recipe for another user
        other_user = get_user_model().objects.create_user(
            'other@example.com',
            'password123',
        )
        create_recipe(user=other_user)
        # Create a sample recipe for the authenticated user
        create_recipe(user=self.user)

        # Make a GET request to retrieve the list of recipes
        res = self.client.get(RECIPES_URL)

        # Retrieve Recipe objects filtered by the authenticated user
        recipes = Recipe.objects.filter(user=self.user)
        # Serialize the filtered Recipe objects to JSON format
        serializer = RecipeSerializer(recipes, many=True)
        # Assert that the request was successful with a 200 OK status code
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # Assert that the response data matches the serialized Recipe data
        self.assertEqual(res.data, serializer.data)

    def test_get_recipe_detail(self):
        """Test get recipe detail."""
        # Create a sample recipe for the authenticated user
        recipe = create_recipe(user=self.user)

        # Generate the URL for the recipe detail view using the recipe ID
        url = detail_url(recipe.id)
        # Make a GET request to retrieve the recipe details
        res = self.client.get(url)

        # Serialize the Recipe object to JSON format using the detailed serializer
        serializer = RecipeDetailSerializer(recipe)
        # Assert that the response data matches the serialized Recipe detail data
        self.assertEqual(res.data, serializer.data)

    def test_create_recipe(self):
        """Test creating a recipe."""

        # Define the payload with the data for creating a new recipe
        payload = {
            'title': 'Sample recipe',        # Title of the recipe
            'time_minutes': 30,              # Time required to prepare the recipe in minutes
            'price': Decimal('5.99'),        # Price of the recipe
        }

        # Make a POST request to create a new recipe using the defined payload
        res = self.client.post(RECIPES_URL, payload)

        # Assert that the response status code is 201 (Created), indicating the recipe was successfully created
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # Retrieve the newly created recipe from the database using the ID returned in the response
        recipe = Recipe.objects.get(id=res.data['id'])

        # Loop through each key-value pair in the payload and assert that the corresponding attribute
        # in the created recipe matches the value from the payload
        for k, v in payload.items():
            self.assertEqual(getattr(recipe, k), v)

        # Assert that the user associated with the recipe is the same as the authenticated user who created it
        self.assertEqual(recipe.user, self.user)