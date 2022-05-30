from django.db import models
from django.forms import CharField
from django.db import models


class UploadImage(models.Model):
    image = models.ImageField(upload_to='images')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploader = models.CharField(max_length=20, blank=True)
    imageURL = models.TextField(max_length=200, default="", blank=True)

    def __str__(self):
        return self.imageURL
