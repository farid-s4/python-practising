from django import forms
from django.forms.fields import EmailField


class ContactForm(forms.Form):
    name = forms.CharField(
        required=True,

        label='Имя',
        max_length=50,
        min_length=2,
        widget=forms.TextInput(attrs={'placeholder':'Enter your name'})
    )
    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        return name
    email = forms.EmailField(
        label='Почта',
        required=True,
        widget=forms.EmailInput(attrs={'placeholder':'Enter your email'}))

    message = forms.CharField(
        required=True,
        label="Сообщение",
        widget=forms.Textarea(attrs={'placeholder':'Enter your message', 'rows':'5'}),
        min_length=10,
        max_length=1000
    )
    def clean_message(self):
        message = self.cleaned_data['message'].strip().lower()
        forbidder_words = ['spam', 'scam', 'hack', 'idiot', 'stupid', 'fake']
        if not message:
            raise forms.ValidationError("Message should not be empty or only spaces")
        for word in forbidder_words:
            if word in message:
                raise forms.ValidationError("Message should not start with '%s'" % word)
        return message



class NoteForm(forms.Form):
    CATEGORY_CHOICES = [
        ('study', 'Study'),
        ('work', 'Work'),
        ('backend', "Backend"),
        ('frontend', 'Frontend'),
    ]
    title = forms.CharField(
        label="Title",
        min_length=5,
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder':'Enter your title'})
    )
    content = forms.CharField(
        label="Content",
        widget=forms.Textarea(attrs={'placeholder':'Enter your content', 'rows':'6'}, ),
        min_length=5,
    )
    tags = forms.CharField(
        label="Tags",
        max_length=200,
        widget=forms.TextInput(attrs={'placeholder':'Enter your tags. Example: django python'})
    )
    category = forms.ChoiceField(
        label="Category",
        choices=CATEGORY_CHOICES,
    )

    def clean_title(self):
        title = self.cleaned_data['title'].strip()
        if title.lower().startswith('test'):
            raise forms.ValidationError("Title should not start with 'test'")
        return title

