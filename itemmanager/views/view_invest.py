from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from itemmanager.models.invest import Investment,  InSection
from itemmanager.forms import  InSectionForm, InvestmentForm
from django.db.models import Sum
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.http import JsonResponse

from django.contrib import messages

@login_required
def isection_list(request):
    if request.method == 'POST':
        isection_id = request.POST.get('isection_id')
        try:
            isection = InSection.objects.get(id=isection_id)
            isection.delete()
            messages.success(request, 'Section deleted successfully.')
        except InSection.DoesNotExist:
            messages.error(request, 'Section not found or could not be deleted.')

    isections = InSection.objects.all()
    total_invest_amount_of_all_isections = Investment.objects.aggregate(total=Sum('amount'))['total'] or 0

    return render(request, 'invest/isection_list.html', {'isections': isections, 'total_invest_amount_of_all_isections': total_invest_amount_of_all_isections})

@login_required
def invest_list(request, isection_id):
    isection = get_object_or_404(InSection, id=isection_id)
    investments = Investment.objects.filter(section=isection)

    total_invest_amount = investments.aggregate(total=Sum('amount'))['total'] or 0
    total_invest_amount_of_all_isections = Investment.objects.aggregate(total=Sum('amount'))['total'] or 0

    if request.method == 'POST':
        investment_id = request.POST.get('invest_id')
        try:
            investment = Investment.objects.get(id=investment_id)
            investment.delete()
            messages.success(request, 'Investment deleted successfully.')
        except Investment.DoesNotExist:
            messages.error(request, 'Investment not found or could not be deleted.')
        return redirect('invest_list', isection_id=isection_id)

    return render(request, 'invest/invest_list.html', {'isection': isection, 'investments': investments, 'total_invest_amount': total_invest_amount, 'total_invest_amount_of_all_isections': total_invest_amount_of_all_isections})


@login_required
def investment_detail(request, insection_id, investment_id):
    investment = get_object_or_404(Investment, id=investment_id)
    isection = get_object_or_404(InSection, id=insection_id)

    if request.method == 'POST':

        if form.is_valid():


                # Update the interest using the calculate_interest method
                investment.interest_rate = investment.calculate_interest()

                # Save the updated invest
                investment.save()

    # Recalculate the total amount after the payment is made
    total_amount = investment.amount + investment.calculate_interest()


    return render(request, 'invest/invest_detail.html', {'isection': isection, 'investment': investment,  'total_amount': total_amount})

@login_required
def iadd_section(request):
    if request.method == 'POST':
        form = InSectionForm(request.POST)
        if form.is_valid():
            isection = form.save()
            return redirect('invest_list', isection_id=isection.id)  # Redirect to the invest_list for the new section
    else:
        form = InSectionForm()

    return render(request, 'invest/iadd_section.html', {'form': form})




@login_required
def add_investment(request, isection_id):
    isection = get_object_or_404(InSection, id=isection_id)

    if request.method == 'POST':
        form = InvestmentForm(request.POST)
        if form.is_valid():
            investment = form.save(commit=False)
            investment.isection = isection
            investment.save()
            return redirect('invest_list', isection_id=isection_id)
    else:
        form = InvestmentForm()
    return render(request, 'invest/add_invest.html', {'isection': isection, 'form': form})

