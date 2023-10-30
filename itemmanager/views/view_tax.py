from django.shortcuts import render
from itemmanager.models.tax import UserProfile

def calculate_tax(request):
    if request.method == 'POST':
        income = float(request.POST.get('income'))
        deductions = float(request.POST.get('deductions', 0))
        exemptions = float(request.POST.get('exemptions', 0))

        taxable_income = income - deductions - exemptions

        if taxable_income <= 250000:
            tax_rate = 0
        elif taxable_income <= 500000:
            tax_rate = 0.05
        elif taxable_income <= 1000000:
            tax_rate = 0.2
        else:
            tax_rate = 0.3

        tax_percentage = tax_rate * 100  # To display as a percentage

        tax_liability = taxable_income * tax_rate

        user_profile = UserProfile(
            annual_income=income,
            deductions=deductions,
            exemptions=exemptions,
            tax_liability=tax_liability,
            tax_percentage=tax_percentage,
        )
        user_profile.save()

        return render(request, 'tax_calculation/tax_result.html', {'user_profile': user_profile})

    return render(request, 'tax_calculation/tax_form.html')
