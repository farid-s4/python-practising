# 3. Формы и валидация
# Используйте ModelForm. Сумма должна быть больше нуля. Дата расхода не может быть в
# будущем.
# Название должно содержать минимум 3 символа после удаления пробелов по краям. Ошибки
# должны отображаться рядом с соответствующими полями
import datetime

from django import forms
from django.forms import ModelForm, DateInput, NumberInput

from tracker.models import Expense


class ExpenseFilterForm(forms.Form):
    search = forms.CharField(
        label='Поиск по названию', required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Название расхода'}),
    )
    category = forms.CharField(
        label='Категория', required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Введите категорию'}),
    )
    payment_method = forms.ChoiceField(label='Способ оплаты', required=False)
    start_date = forms.DateField(
        label='Дата с', required=False, widget=DateInput(attrs={'type': 'date'}),
    )
    end_date = forms.DateField(
        label='Дата по', required=False, widget=DateInput(attrs={'type': 'date'}),
    )

    def __init__(self, *args, payment_methods=(), **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['payment_method'].choices = [('', 'Все способы')] + [
            (value, value) for value in payment_methods
        ]

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_date and end_date and start_date > end_date:
            self.add_error('end_date', 'Конечная дата не может быть раньше начальной.')
        return cleaned_data


class ExpenseForm(ModelForm):
    class Meta:
        model = Expense
        fields = [
            'name',
            'amount',
            'payment_method',
            'comment',
            'category',
            'payment_date',
        ]
        labels = {
            'category': 'Категория',
        }
        widgets = {
            'created_at': DateInput(attrs={'type': 'date'}),
            'amount': NumberInput(attrs={'type': 'number'}),
            'payment_date': DateInput(attrs={'type': 'date'}),
        }
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
