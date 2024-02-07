from django.shortcuts import render, redirect, get_object_or_404
from itemmanager.models.income import Income, IncSection, MonthlyIncome
from itemmanager.forms import IncomeForm, IncSectionForm, MonthlyIncomeForm
from django.db.models import Sum
from decimal import Decimal
from django.db.models import F, ExpressionWrapper, DecimalField
from django.db.models import Sum, Value

def apply_gst(income_amount):
    # Calculate GST of 18%
    gst_rate = Decimal('0.18')
    gst_amount = income_amount * gst_rate
    total_amount = income_amount + gst_amount
    return total_amount


def incsection_list(request):
    incsections = IncSection.objects.all()

    total_income = Income.objects.aggregate(total=Sum('amount'))['total']
    total_income = total_income or Decimal('0')  # Convert to Decimal

    # Apply GST
    total_income_with_gst = apply_gst(total_income)

    # Convert to float for session storage
    total_income_float = float(total_income_with_gst)

    # Store the value in the session
    request.session['total_income'] = total_income_float

    if request.method == 'POST' and 'delete_incsection' in request.POST:
        incsection_id = request.POST['delete_incsection']
        incsection = IncSection.objects.get(pk=incsection_id)
        incsection.delete()
        return redirect('incsection_list')

    return render(request, 'incsection_list.html', {'incsections': incsections, 'total_income': total_income_with_gst})

def add_incsection(request):
    if request.method == 'POST':
        form = IncSectionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('incsection_list')
    else:
        form = IncSectionForm()

    return render(request, 'add_incsection.html', {'form': form})

def income_list(request, incsection_id):
    incsection = get_object_or_404(IncSection, pk=incsection_id)
    incomes = Income.objects.filter(incsection=incsection)

    # Apply GST to each income
    for income in incomes:
        income.amount_with_gst = apply_gst(income.amount)

    incsection = IncSection.objects.get(pk=incsection_id)
    total_income = incomes.aggregate(total=Sum('amount'))['total']

    if total_income is not None:
        # Apply GST to the total income
        total_income_with_gst = apply_gst(total_income)
    else:
        total_income_with_gst = Decimal('0.00')

    return render(request, 'income_list.html', {'incomes': incomes, 'total_income': total_income_with_gst, 'incsection': incsection})


def add_income(request, incsection_id):
    incsection = IncSection.objects.get(pk=incsection_id)
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            form.instance.incsection = incsection
            form.save()
            return redirect('income_list', incsection_id=incsection_id)
    else:
        form = IncomeForm()

    incomes = Income.objects.filter(incsection=incsection)
    total_income = sum(income.amount for income in incomes)

    # Apply GST to the total income
    total_income_with_gst = apply_gst(total_income)

    return render(request, 'add_income.html', {'incsection': incsection, 'form': form, 'incomes': incomes, 'total_income': total_income_with_gst})

def edit_income(request, income_id):
    income = get_object_or_404(Income, pk=income_id)

    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            return redirect('income_list', incsection_id=income.incsection.id)
    else:
        form = IncomeForm(instance=income)

    return render(request, 'edit_income.html', {'form': form, 'income': income})

def delete_income(request, income_id):
    income = get_object_or_404(Income, pk=income_id)
    incsection_id = income.incsection.id
    if request.method == 'POST':
        income.delete()
        return redirect('income_list', incsection_id=incsection_id)
    return render(request, 'delete_income.html', {'income': income, 'incsection_id': incsection_id})

def monthly_income_list(request):
    monthly_incomes = MonthlyIncome.objects.all()
    total_monthly_income = monthly_incomes.aggregate(total=Sum('amount'))['total'] or Decimal('0')

    # Calculate the total of all sections' incomes
    total_section_income = Income.objects.aggregate(total=Sum('amount'))['total'] or Decimal('0')



    return render(request, 'monthlyincome/monthly_income_list.html', {'monthly_incomes': monthly_incomes, 'total_monthly_income': total_monthly_income})

from decimal import Decimal
from itemmanager.models.income import Income, MonthlyIncome

def calculate_total_income_pool():
    # Calculate the total of all sections' incomes
    total_section_income = Income.objects.aggregate(total=Sum('amount'))['total'] or Decimal('0')

    # Calculate the total monthly income
    total_monthly_income = MonthlyIncome.objects.aggregate(total=Sum('amount'))['total'] or Decimal('0')

    # Calculate the combined total income pool
    total_income_pool = total_monthly_income + total_section_income

    return total_income_pool

def add_monthly_income(request):
    if request.method == 'POST':
        form = MonthlyIncomeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('monthly_income_list')
    else:
        form = MonthlyIncomeForm()

    return render(request, 'monthlyincome/add_monthly_income.html', {'form': form})

from django.http import Http404

def delete_monthly_income(request, monthly_income_id):
    monthly_income = get_object_or_404(MonthlyIncome, pk=monthly_income_id)

    if request.method == 'POST':
        monthly_income.delete()
        return redirect('monthly_income_list')

    return render(request, 'monthlyincome/delete_monthly_income.html', {'monthly_income': monthly_income})

def edit_monthly_income(request, monthly_income_id):
    monthly_income = get_object_or_404(MonthlyIncome, pk=monthly_income_id)

    if request.method == 'POST':
        form = MonthlyIncomeForm(request.POST, instance=monthly_income)
        if form.is_valid():
            form.save()
            return redirect('monthlyincome/monthly_income_list')
    else:
        form = MonthlyIncomeForm(instance=monthly_income)

    return render(request, 'monthlyincome/edit_monthly_income.html', {'form': form, 'monthly_income': monthly_income})
