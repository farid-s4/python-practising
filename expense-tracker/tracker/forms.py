# 3. Формы и валидация
# Используйте ModelForm. Сумма должна быть больше нуля. Дата расхода не может быть в
# будущем.
# Название должно содержать минимум 3 символа после удаления пробелов по краям. Ошибки
# должны отображаться рядом с соответствующими полями
import datetime

from django import forms
class TrackerForm(forms.Form):
    name = forms.CharField(
        label='Name',
        max_length=100,
        min_length=3,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        if len(name) < 3:
            raise forms.ValidationError('Name must be at least 3 characters long.')
        return name
    def clean_payment_date(self):
        payment_date = self.cleaned_data['payment_date']
        if payment_date < datetime.date.today():
            raise forms.ValidationError('Payment date must be in the future.')
        return payment_date
    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount < 0:
            raise forms.ValidationError('Amount must be positive.')
        return amount
