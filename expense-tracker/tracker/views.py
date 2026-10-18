from datetime import timezone
from multiprocessing import context

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from accounts import forms
from tracker.forms import ExpenseFilterForm, ExpenseForm
from tracker.models import Expense


def index(request):
    return render(request, 'expense_tracker/home.html')
def home(request):
    return render(request, 'expense_tracker/home.html')

@login_required
def expenses_list(request):
    user_expenses = Expense.objects.filter(author=request.user)
    filter_form = ExpenseFilterForm(
        request.GET or None,
        payment_methods=user_expenses.order_by('payment_method').values_list('payment_method', flat=True),
    )
    expenses = user_expenses.order_by('-created_at')

    if filter_form.is_valid():
        filters = filter_form.cleaned_data
        if filters['search']:
            expenses = expenses.filter(name__icontains=filters['search'])
        if filters['category']:
            expenses = expenses.filter(category__icontains=filters['category'])
        if filters['payment_method']:
            expenses = expenses.filter(payment_method=filters['payment_method'])
        if filters['start_date']:
            expenses = expenses.filter(payment_date__gte=filters['start_date'])
        if filters['end_date']:
            expenses = expenses.filter(payment_date__lte=filters['end_date'])
    amount=0
    for expense in expenses:
        amount+=expense.amount
    return render(request, 'expense_tracker/expenses.html', {
        'expenses': expenses,
        'filter_form': filter_form,
        'amount': amount,
    })

@login_required
def expense_detail(request, expense_id):
    expense = Expense.objects.get(id=expense_id, author=request.user)
    return render(request, 'expense_tracker/expense_detail.html', {'expense': expense})
@login_required
def create_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.author = request.user
            expense.save()
            messages.success(request, 'Expense created successfully')
            return redirect('tracker:expense_detail', expense_id=expense.id)
    else:
        form = ExpenseForm()
    return render(
        request,
        'expense_tracker/create_expense.html',
        {'form': form}
    )
