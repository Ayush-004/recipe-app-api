"""
URL mappings for the user API.
"""
from django.urls import path  # Importing the path function to define URL patterns
from user import views  # Importing the views from the user app


# Define a namespace for the user-related URLs, useful when referring to these URLs elsewhere in the project
app_name = 'user'

# Define the URL patterns that map to the corresponding views
urlpatterns = [
    # Map the 'create/' URL to the CreateUserView, and name this URL pattern 'create'
    path('create/', views.CreateUserView.as_view(), name='create'),
    # The .as_view() method is used to convert the class-based view into a Django-view that can be called when the URL is requested
    path('token/', views.CreateTokenView.as_view(), name='token'),  # Map the 'token/' URL to the CreateTokenView
    path('me/', views.ManageUserView.as_view(), name='me'), # Map the 'me/' URL to the ManageUserView
]