
from django.shortcuts import render, redirect, get_object_or_404
from itemmanager.models.income import Income, IncSection
from itemmanager.forms import IncomeForm, IncSectionForm
from django.db.models import Sum



def incsection_list(request):
    incsections = IncSection.objects.all()
    total_income = Income.objects.aggregate(total=Sum('amount'))['total']
    
    if request.method == 'POST' and 'delete_incsection' in request.POST:
        incsection_id = request.POST['delete_incsection']
        incsection = IncSection.objects.get(pk=incsection_id)
        incsection.delete()
        return redirect('incsection_list')
    
    return render(request, 'incsection_list.html', {'incsections': incsections, 'total_income': total_income})

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
    incsection = IncSection.objects.get(pk=incsection_id)
    total_income = incomes.aggregate(total=Sum('amount'))['total']
    return render(request, 'income_list.html', {'incomes': incomes, 'total_income': total_income, 'incsection':incsection})

def add_income(request,incsection_id):
    incsection = IncSection.objects.get(pk=incsection_id)
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            form.instance.incsection = incsection
            form.save()
            return redirect('income_list',incsection_id=incsection_id)
    else:
        form = IncomeForm()

    incomes = Income.objects.filter(incsection=incsection)
    total_income = sum(income.amount for income in incomes)

    return render(request, 'add_income.html', {'incsection': incsection, 'form': form, 'incomes': incomes, 'total_income': total_income})


def delete_income(request, income_id):
    income = get_object_or_404(Income, pk=income_id)
    incsection_id = income.incsection.id
    if request.method == 'POST':
        income.delete()
        return redirect('income_list',incsection_id=incsection_id)
    return render(request, 'delete_income.html', {'income': income, 'incsection_id':incsection_id})
