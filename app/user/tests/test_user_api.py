"""
Tests for the user API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse # used to resolve the url

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create') #api url to test
TOKEN_URL=reverse('user:token') #url to generate token
ME_URL = reverse('user:me') #url to get user profile


def create_user(**params):# flexibility to add any number of params
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params) #creating a user with the params we pass


class PublicUserApiTests(TestCase):#unautenthicated tests, like registering a new user
    """Test the public features of the user API."""

    def setUp(self):
        self.client = APIClient()#APIClient for testing

    def test_create_user_success(self):
        """Test creating a user is successful."""
        payload = {#test payload to pass to API
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        res = self.client.post(CREATE_USER_URL, payload)#HTTP post req to CREATE_USER_URL

        self.assertEqual(res.status_code, status.HTTP_201_CREATED) #checking if 201 created occurs, for success in creating objects in data
        user = get_user_model().objects.get(email=payload['email'])#retrivers object with email address as the payload
        self.assertTrue(user.check_password(payload['password'])) #if user successful, basically checking password
        self.assertNotIn('password', res.data) #password hash not returned

    def test_user_with_email_exists_error(self):
        """Test error returned if user with email exists."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload) # post payload to the URL

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST) # we get bad request from API if email already existed

    def test_password_too_short_error(self):
        """Test an error is returned if password less than 5 chars."""
        payload = {
            'email': 'test@example.com',
            'password': 'pw',
            'name': 'Test name',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter( # we expected that the user shouldn't exist
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)#the use isn't existing
    def test_create_token_for_user(self):
        """Test generates token for valid credentials."""
        # Set up user details to be used for creating a new user
        user_details = {
            'name': 'Test Name',
            'email': 'test@example.com',
            'password': 'test-user-password123',
        }
        # Create a new user using the provided details
        create_user(**user_details)

        # Prepare the payload with the email and password to send to the token generation endpoint
        payload = {
            'email': user_details['email'],
            'password': user_details['password'],
        }
        # Send a POST request to the token URL with the payload to generate an authentication token
        res = self.client.post(TOKEN_URL, payload)

        # Assert that the response contains a 'token' field in the response data
        self.assertIn('token', res.data)
        # Assert that the response status code is 200 OK, indicating success
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Test returns error if credentials invalid."""
        # Create a user with a known email and password
        create_user(email='test@example.com', password='goodpass')

        # Prepare a payload with the correct email but an incorrect password
        payload = {'email': 'test@example.com', 'password': 'badpass'}
        # Send a POST request to the token URL with the payload
        res = self.client.post(TOKEN_URL, payload)

        # Assert that the response does not contain a 'token' field (indicating failure)
        self.assertNotIn('token', res.data)
        # Assert that the response status code is 400 BAD REQUEST, indicating invalid credentials
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_email_not_found(self):
        """Test error returned if user not found for given email."""
        # Prepare a payload with an email that does not exist in the database and a password
        payload = {'email': 'test@example.com', 'password': 'pass123'}
        # Send a POST request to the token URL with the payload
        res = self.client.post(TOKEN_URL, payload)

        # Assert that the response does not contain a 'token' field (indicating failure)
        self.assertNotIn('token', res.data)
        # Assert that the response status code is 400 BAD REQUEST, indicating the email was not found
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Test posting a blank password returns an error."""
        # Prepare a payload with a valid email but a blank password
        payload = {'email': 'test@example.com', 'password': ''}
        # Send a POST request to the token URL with the payload
        res = self.client.post(TOKEN_URL, payload)

        # Assert that the response does not contain a 'token' field (indicating failure)
        self.assertNotIn('token', res.data)
        # Assert that the response status code is 400 BAD REQUEST, indicating invalid input (blank password)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    def test_retrieve_user_unauthorized(self):
        """Test authentication is required for users."""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication."""

    def setUp(self):  # Set up a user and client for the tests, called before each test
        """Set up a user and client for the tests."""
        # Create a user for authentication purposes
        self.user = create_user(
            email='test@example.com',
            password='testpass123',
            name='Test Name',
        )
        # Initialize the APIClient, which will be used to make API requests
        self.client = APIClient()
        # Force authentication for the client with the created user
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving the profile for the logged-in user."""
        # Make a GET request to the ME_URL to retrieve the user's profile
        res = self.client.get(ME_URL)

        # Assert that the request was successful (HTTP 200 OK)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # Assert that the returned data matches the user's name and email
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email,
        })

    def test_post_me_not_allowed(self):
        """Test POST is not allowed for the me endpoint."""
        # Make a POST request to the ME_URL, which should not be allowed, as POST is used for creating objects
        res = self.client.post(ME_URL, {})

        # Assert that the request is not allowed (HTTP 405 Method Not Allowed)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for the authenticated user."""
        # Prepare the payload with updated user information
        payload = {'name': 'Updated name', 'password': 'newpassword123'}

        # Make a PATCH request to the ME_URL with the updated information
        res = self.client.patch(ME_URL, payload)

        # Refresh the user object from the database to reflect changes made by the PATCH request
        self.user.refresh_from_db()
        # Assert that the user's name has been updated as expected
        self.assertEqual(self.user.name, payload['name'])
        # Assert that the user's password has been updated and is correctly hashed
        self.assertTrue(self.user.check_password(payload['password']))
        # Assert that the request was successful (HTTP 200 OK)
        self.assertEqual(res.status_code, status.HTTP_200_OK)