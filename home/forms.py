from django.db import models
from django.forms import fields
from .models import UploadImage
from django import forms


class UploadImageForm(forms.ModelForm):
    class Meta:
        # To specify the model to be used to create form
        model = UploadImage
        # It includes all the fields of model
        fields = ("image", "uploader", "imageURL")
        widgets = {
            "image": forms.FileInput(attrs={
                'class': 'form-control'
            }),
            "uploader": forms.TextInput(attrs={
                'class': 'form-control hide',
                "id": "uploader",
                'hidden': True
            }),
            "imageURL": forms.TextInput(attrs={
                'class': 'form-control hide',
                "id": "imageURL",
                'hidden': True
            })
        }
