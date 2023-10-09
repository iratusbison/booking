
from django.shortcuts import render, redirect, get_object_or_404
from itemmanager.models.expense import Expense
from itemmanager.forms import ExpenseForm
from django.db.models import Sum

def expense_list(request):
    expenses = Expense.objects.all()

    total_expenses = expenses.aggregate(total=Sum('amount'))['total']
    return render(request, 'expense_list.html', {'expenses': expenses, 'total_expenses': total_expenses})

def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'add_expense.html', {'form': form})

def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, pk=expense_id)
    if request.method == 'POST':
        expense.delete()
        return redirect('expense_list')
    return render(request, 'delete_expense.html', {'expense': expense})
