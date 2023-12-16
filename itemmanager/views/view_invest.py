from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from itemmanager.models.invest import Investment,  InSection, RD, RDSection
from itemmanager.forms import  InSectionForm, InvestmentForm, RDSectionForm, RDForm
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

    total_invest_amount_of_all_isections = float(total_invest_amount_of_all_isections)
    request.session['total_invest_amount_of_all_isections'] = total_invest_amount_of_all_isections

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



@login_required
def rdsection_list(request):
    if request.method == 'POST':
        rdsection_id = request.POST.get('rdsection_id')
        try:
            rdsection = RDSection.objects.get(id=rdsection_id)
            rdsection.delete()
            messages.success(request, 'RD Section deleted successfully.')
        except RDSection.DoesNotExist:
            messages.error(request, 'RD Section not found or could not be deleted.')

    rdsections = RDSection.objects.all()
    total_rd_amount_of_all_rdsections = RD.objects.aggregate(total=Sum('principal_amount'))['total'] or 0

    total_rd_amount_of_all_rdsections = float(total_rd_amount_of_all_rdsections)
    request.session['total_rd_amount_of_all_rdsections'] = total_rd_amount_of_all_rdsections

    return render(request, 'invest/rdsection_list.html', {'rdsections': rdsections, 'total_rd_amount_of_all_rdsections': total_rd_amount_of_all_rdsections})


@login_required
def rd_list(request, rdsection_id):
    rdsection = get_object_or_404(RDSection, id=rdsection_id)
    rds = RD.objects.filter(section=rdsection)

    total_rd_amount = rds.aggregate(total=Sum('principal_amount'))['total'] or 0
    total_rd_amount_of_all_rdsections = RD.objects.aggregate(total=Sum('principal_amount'))['total'] or 0

    if request.method == 'POST':
        rd_id = request.POST.get('rd_id')
        try:
            rd = RD.objects.get(id=rd_id)
            rd.delete()
            messages.success(request, 'RD Investment deleted successfully.')
        except RD.DoesNotExist:
            messages.error(request, 'RD Investment not found or could not be deleted.')

        return redirect('rd_list', rdsection_id=rdsection_id)

    return render(request, 'invest/rd_list.html', {'rdsection': rdsection, 'rds': rds, 'total_rd_amount': total_rd_amount, 'total_rd_amount_of_all_rdsections': total_rd_amount_of_all_rdsections})


@login_required
def rd_detail(request, rdsection_id, rd_id):
    rd = get_object_or_404(RD, id=rd_id)
    rdsection = get_object_or_404(RDSection, id=rdsection_id)

    # Calculate the total amount using the calculate_total_amount method
    total_amount = rd.calculate_total_amount()
    print("Total Amount:", total_amount)

    return render(request, 'invest/rd_detail.html', {'rdsection': rdsection, 'rd': rd, 'total_amount': total_amount})

@login_required
def Radd_section(request):
    if request.method == 'POST':
        form = RDSectionForm(request.POST)
        if form.is_valid():
            rdsection = form.save()
            return redirect('rd_list', rdsection_id=rdsection.id)
    else:
        form = InSectionForm()

    return render(request, 'invest/rdadd_section.html', {'form': form})



@login_required
def add_rd(request, rdsection_id):
    rdsection = get_object_or_404(RDSection, id=rdsection_id)

    if request.method == 'POST':
        form = RDForm(request.POST)
        if form.is_valid():
            rd = form.save(commit=False)
            rd.section = rdsection
            rd.save()
            return redirect('rd_list', rdsection_id=rdsection_id)
    else:
        form = RDForm()

    return render(request, 'invest/add_rd.html', {'rdsection': rdsection, 'form': form})





