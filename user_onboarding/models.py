from django.db import models


POSTS = (
    ("Moderator", "Moderator"),
    ("Railway Admin", "Railway Admin"),
    ("Normal User", "Normal User"),
    ("Superuser", "Superuser"),
)


class Request_User(models.Model):
    user_name = models.CharField(
        max_length=100, default=None, null=True, blank=True, unique=True)
    user_email = models.CharField(
        max_length=100, default=None, null=True, blank=True, unique=True)
    user_password = models.CharField(
        max_length=100, default=None, null=True, blank=True)
    for_post = models.CharField(
        max_length=100, choices=POSTS, default=None, null=True, blank=True)
    approved = models.BooleanField(default=False, null=True, blank=True)
    seen = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return str(self.user_name)


class PhoneNumber(models.Model):
    user = models.OneToOneField(
        Request_User, on_delete=models.CASCADE, related_name='phone')
    mobile_number = models.CharField(
        max_length=12, default=None, null=True, blank=True, unique=True)

    def __str__(self):
        return str(self.mobile_number)
