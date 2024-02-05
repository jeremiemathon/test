from django.db import models
from django.conf import settings
from django.utils.text import slugify
import uuid
import os

class Directory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='subdirectories', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def is_root_directory(self):
        return self.parent is None

    def get_system_path(self):
        if self.is_root_directory():
            return settings.LIBRARY_ROOT
        else:
            parent_path = self.parent.get_system_path()
            return os.path.join(parent_path, self.name)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class Document(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    
    directory = models.ForeignKey(Directory, null=True, blank=True, related_name='documents', on_delete=models.CASCADE)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Assuming you have a user model
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_upload_path(self, filename):
        directory_path = self.directory.get_system_path()
        directory_path = directory_path.lstrip('/')
        return os.path.join(directory_path, filename)

    file = models.BinaryField()  # You might want to customize the upload path