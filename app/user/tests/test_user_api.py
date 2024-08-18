"""
Tests for the user API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse # used to resolve the url

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create') #api url to test


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