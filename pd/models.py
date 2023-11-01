import random
from django.db import models


def generate_default_pk_name_location():
    return f"{random.randint(123456789, 987654321)}"


class FileData(models.Model):
    name = models.CharField(max_length=255)
    content = models.TextField()
    location = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    pk_name_location = models.CharField(
        max_length=510,
        primary_key=True,
        default=generate_default_pk_name_location
    )

    def save(self, *args, **kwargs):
        self.pk_name_location = f"{self.name}_{self.location}"
        super(FileData, self).save(*args, **kwargs)


class FolderData(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    num_files = models.IntegerField()
    files = models.ManyToManyField(FileData)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.location = self.location.rstrip('\\')
        self.pk = f"{self.name}_{self.location}"
        super(FolderData, self).save(*args, **kwargs)

    def __str__(self):
        return self.location