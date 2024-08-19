'''
Django admin customization for the User model.
'''

from django.contrib import admin  # Importing the Django admin module
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin  # Importing the default UserAdmin class to extend
from django.utils.translation import gettext_lazy as _  # Importing for handling translations of field labels

from core import models  # Importing the models from the core app, assuming User model is defined here

# Define a custom UserAdmin class to customize the admin interface for the User model
class UserAdmin(BaseUserAdmin):
    '''Define the admin pages for users.'''

    # Specify the default ordering of the user list in the admin interface by the 'id' field
    ordering = ['id']

    # Define the columns to be displayed in the user list view in the admin interface
    list_display = ['email', 'name']

    # Define the layout and grouping of fields on the user detail/edit page in the admin interface
    fieldsets = (
        # Group 1: Contains email and password fields, shown without a specific title
        (None, {'fields': ('email', 'password')}),

        # Group 2: Contains permission-related fields, with a translated title "Permissions"
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),

        # Group 3: Contains important dates like the last login, with a translated title "Important dates"
        (_('Important dates'), {'fields': ('last_login',)}),
    )

    # Specify fields that should be read-only in the admin interface
    readonly_fields = ['last_login']

    # Define the layout and fields for the user creation form in the admin interface
    add_fieldsets = (
        # Group the fields with no specific title and make them wide for better layout
        (None, {
            'classes': ('wide',),  # Adds CSS class 'wide' to make the form fields wider
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }),
    )

# Register the User model with the custom UserAdmin class, replacing the default admin behavior
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Recipe)