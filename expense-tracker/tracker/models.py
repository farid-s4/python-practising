from django.db import models
from django.conf import settings

# 1. Модель Expense
# Название расхода; сумма; категория (продукты, транспорт, обучение, развлечения, здоровье,
# другое); способ оплаты (наличные или карта); дата расхода; необязательный комментарий; дата
# создания записи; владелец записи
class Expense(models.Model):
    name = models.CharField(max_length=200, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=200)
    payment_method = models.CharField(max_length=200)
    payment_date = models.DateField(
        null=True,
        blank=True,
        help_text="Date of payment",
    )
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
    )

    class Meta:
        verbose_name = "Expense"
        verbose_name_plural = 'Expenses'

