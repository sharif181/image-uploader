from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    UserManager,
    PermissionsMixin
)

from django.core.validators import MaxValueValidator, MinValueValidator


BUILT_IN_TIERS = (
    ('basic', 'Basic'),
    ('premium', 'Premium'),
    ('enterprise', 'Enterprise')
)

class ArbitaryTier(models.Model):
    tier_name = models.CharField(max_length=255)
    thumbnail_size = models.IntegerField()
    is_original_link = models.BooleanField(default=False)
    is_generate_link = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.tier_name}-{self.thumbnail_size}"


class UserManager(UserManager):

    def create_superuser(self, username, email, password):
        if username is None:
            raise TypeError("Username field cannot be empty. ")
        if password is None:
            raise TypeError("Please enter password. ")

        user = self.create_user(username,email=email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

    def create_user(self, username,email, password=None):
        if username is None:
            raise TypeError("Username field cannot be empty. ")

        user = self.model(username=username, email=email)
        user.set_password(password)
        user.save()

        return user


class User(AbstractUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, db_index=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    build_in_tier = models.CharField(max_length=10, choices=BUILT_IN_TIERS, default='basic', null=True, blank=True)
    arbitary_tier = models.OneToOneField(ArbitaryTier, on_delete=models.CASCADE, blank=True, null=True)

    USERNAME_FIELD = 'username'

    objects = UserManager()

    def __str__(self):
        return self.username



def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)

class FileUpload(models.Model):
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(
        max_length=80, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image_url = models.ImageField(upload_to=upload_to)

    def __str__(self):
        return f'{self.title} - {self.id}' 


class GenerateLink(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(FileUpload, on_delete=models.CASCADE)
    create_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    link_duration = models.IntegerField(default=300,
                                        validators=[MaxValueValidator(30000), MinValueValidator(300)])

    def __str__(self):
        return f'{self.image.image_url} - {self.create_at}'