from django import forms

CATEGORIES = [
    ('Education', 'Education'),
    ('Technology', 'Technology'),
    ('Sport', 'Sport'),
    ('Entertainment', 'Entertainment'),
    ('Other', 'Other'),
]

class EventForm(forms.Form):
    name = forms.CharField(
        label='Event Name',
        max_length=50,
        min_length=5,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        required = True,
    )
    description = forms.CharField(
        label='Event Description',
        max_length=150,
        min_length=5,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    title = forms.CharField(
        label='Event Title',
        max_length=500,
        min_length=5,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        required=True,
    )
    category = forms.ChoiceField(
        choices=CATEGORIES,
        label='Event Category',
    )
    location = forms.CharField(
        label='Event Location',
        max_length=150,
        min_length=5,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    def clean_title(self):
        title = self.cleaned_data['title']

        if title.lower() == 'test':
            raise forms.ValidationError(
                'Название события не может быть "test".'
            )

        return title

    def clean_location(self):
        location = self.cleaned_data['location']

        if len(location.strip()) < 3:
            raise forms.ValidationError(
                'Место проведения должно содержать минимум 3 символа.'
            )

        return location