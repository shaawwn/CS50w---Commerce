from django import forms
from django.forms import ModelForm
from .models import Listing

class ListingForm(forms.ModelForm):

    class Meta:
        model = Listing
        fields = (
            'title',
            'description',
            'starting_bid',
            'category',
            'image', 
        )

        labels = {
            'title': 'Title',
            'description': 'Description',
            'starting_bid': 'Starting Bid',
            'category': 'Category',
            'image': 'Image'
        }

        widgets = {
            'title': forms.TextInput(attrs=({'class': 'form-input'})),
            'description': forms.Textarea(attrs={'class': 'form-input', 'cols': 40, 'rows': 10}),
            'starting_bid': forms.NumberInput(attrs=({'class': 'form-input'})), # (TextInput in some cases)
            'category': forms.TextInput(attrs={'class': 'form-input'}),
            'image': forms.ClearableFileInput(attrs=({'class': 'form-input'}))
        }