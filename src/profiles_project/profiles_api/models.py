from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

# Create your models here.

class UserProfileManager(BaseUserManager):
    """ Helps Django work with our custom user model """

    def create_user(self, email, name, password=None):
        """ Creates a new user profile object """

        # check if email address doesn't exist
        if not email:
            raise ValueError('Users must have an email address.')

        # Normalizing the email address
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        # Encrypts password so it is stored as a hash in database
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, email, name, password):
        """ Creates and saves a new superuser with given details. """

        user = self.create_user(email, name, password)

        # assign two vars to user
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user

class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Represents a "user profile" inside our system."""
    # Define fields
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Assign object manager
    objects = UserProfileManager()

    # login with email address
    USERNAME_FIELD = 'email'

    # Define required fields - must be a list
    REQUIRED_FIELDS = ['name']

    # Create helper functions
    def get_full_name(self):
        """ Used to get a user's full name. """

        return self.name

    def get_short_name(self):
        """ Used to get a user's short name. """

        return self.name

    # Create str function so know how to return name
    def __str__(self):
        """ Django uses this when it needs to convert the object to a string"""

        return self.email

class ProfileFeedItem(models.Model):
    """ Profile status update. """

    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    status_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """ Return the model as a string. """

        return self.status_text
        
