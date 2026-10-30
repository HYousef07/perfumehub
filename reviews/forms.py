
from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['rating', 'comment']

        widgets = {
            'rating': forms.Select(
                attrs={
                    'class': 'form-select',
                }
            ),

            'comment': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Write your review...',
                    'rows': 4,
                }
            ),
        }

        labels = {
            'rating': 'Your Rating',
            'comment': 'Your Review',
        }