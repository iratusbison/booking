from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from itemmanager.models.loan import Loan, Payment, Section
from itemmanager.forms import LoanForm, PaymentForm, SectionForm
from django.db.models import Sum
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages


@login_required
def section_list(request):
    sections = Section.objects.all()
    total_loan_amount_of_all_sections = Loan.objects.aggregate(total=Sum('amount'))['total'] or 0
    
    return render(request, 'loan/section_list.html', {'sections': sections, 'total_loan_amount_of_all_sections': total_loan_amount_of_all_sections})
    
@login_required
def loan_list(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    loans = Loan.objects.filter(section=section)
    
    total_loan_amount = loans.aggregate(total=Sum('amount'))['total'] or 0
    total_loan_amount_of_all_sections = Loan.objects.aggregate(total=Sum('amount'))['total'] or 0


    if request.method == 'POST':
        loan_id = request.POST.get('loan_id')
        loan = get_object_or_404(Loan, id=loan_id)
        loan.delete()
        return redirect('loan_list', section_id=section_id)

    return render(request, 'loan/loan_list.html', {'section': section, 'loans': loans, 'total_loan_amount': total_loan_amount, 'total_loan_amount_of_all_sections': total_loan_amount_of_all_sections})


@login_required
def loan_detail(request, section_id, loan_id):
    loan = get_object_or_404(Loan, id=loan_id)
    section = get_object_or_404(Section, id=section_id)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.loan = loan
            payment.save()

            # Update the loan balance and interest based on the payment type
            if payment.payment_type == 'Installment':
                # Subtract the payment amount from the loan balance
                loan.amount -= payment.amount

                # Update the interest using the calculate_interest method
                loan.interest_rate = loan.calculate_interest()

                # Save the updated loan
                loan.save()

    # Recalculate the total amount after the payment is made
    total_amount = loan.amount + loan.calculate_interest()

    payments = Payment.objects.filter(loan=loan)

    # Calculate the reduced total amount
    reduced_total_amount = total_amount - sum(payment.amount for payment in payments if payment.payment_type == 'Installment')

    return render(request, 'loan/loan_detail.html', {'section': section, 'loan': loan, 'payments': payments, 'total_amount': total_amount, 'reduced_total_amount': reduced_total_amount})

@login_required
def add_section(request):
    if request.method == 'POST':
        form = SectionForm(request.POST)
        if form.is_valid():
            section = form.save()
            return redirect('loan_list', section_id=section.id)  # Redirect to the loan_list for the new section
    else:
        form = SectionForm()

    return render(request, 'loan/add_section.html', {'form': form})
    
    
@login_required
def delete_section(request, section_id):
    section = get_object_or_404(Section, id=section_id)

    if request.method == 'POST':
        # Delete the section
        section.delete()

        # Optionally, add a success message
        messages.success(request, 'Section deleted successfully.')

        return redirect('section_list')  # Redirect to the section list page or another appropriate URL

    return render(request, 'loan/section_delete_confirmation.html', {'section': section})


@login_required
def add_loan(request, section_id):
    section = get_object_or_404(Section, id=section_id)

    if request.method == 'POST':
        form = LoanForm(request.POST)
        if form.is_valid():
            loan = form.save(commit=False)
            loan.section = section
            loan.save()
            return redirect('loan_list', section_id=section_id)
    else:
        form = LoanForm()
    return render(request, 'loan/add_loan.html', {'section': section, 'form': form})

@login_required
def make_payment(request, section_id, loan_id):
    section = get_object_or_404(Section, id=section_id)
    loan = get_object_or_404(Loan, id=loan_id)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.loan = loan
            payment.save()

            # Update the loan balance and interest as needed

            return redirect('loan_detail', section_id=section_id, loan_id=loan_id)

    form = PaymentForm()
    return render(request, 'loan/payment_form.html', {'section': section, 'loan': loan, 'form': form})

@login_required
def delete_payment(request, section_id, loan_id):
    if request.method == 'POST':
        payment_id = request.POST.get('payment_id')
        try:
            payment = Payment.objects.get(id=payment_id)
            payment.delete()
        except Payment.DoesNotExist:
            # Handle the case where the payment does not exist
            pass

    return redirect('loan_detail', section_id=section_id, loan_id=loan_id)