from datetime import timezone

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from tracker.models import Expense


def index(request):
    return render(request, 'expense_tracker/home.html')

@login_required
def expenses_list(request):
    expenses = Expense.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'expense_tracker/expenses.html', {'expenses': expenses})
