from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager



class UserProfileManager(BaseUserManager):
    """
    Helps Django to work with our custom user model.
    """
    def create_user(self, email, name, password=None):
        """
        Creates a new user profile object
        """
        if not email:
            raise ValueError('User must have email address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """
        Creates a new superuser profile object
        """
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """
        Used to get a users full name
        """
        return self.name

    def get_short_name(self):
        """
        Used to get a users short name
        """
        return self.name

    def __str__(self):
        return self.email


class ProfileFeedItem(models.Model):
    """
    Profile status update
    """
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    status_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Return the model as a string
        """
        return self.status_text


class Lyrics(models.Model):
    """
    Song lyrics
    """
    artist = models.CharField(max_length=255)
    song_title = models.CharField(max_length=255)
    song_lyrics = models.CharField(max_length=1023)
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    lyrics_collection = models.ForeignKey('LyricsCollection', related_name='lyrics_list', on_delete=models.CASCADE)
    public = models.BooleanField(default=True)
    video_url = models.URLField(max_length=255, blank=True)


class LyricsCollection(models.Model):
    """
    Collection of song lyrics
    """
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title
