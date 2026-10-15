from django import forms
from .models import Review, SkillProposal, Favorites


class ProposalForm(forms.ModelForm):
    class Meta:
        model = SkillProposal
        fields = [
            'name',
            'image',
            'description',
            'level',
            'online',
            'lesson_duration',
            'category'
        ]
        labels = {
            'category': 'Категория',
        }
        widgets = {
            'category': forms.Select(
                attrs={
                    'class': 'form-control',
                },
            ),
        }



class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            'rating',
            'review'
        ]
