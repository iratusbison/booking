from django.shortcuts import render
from itemmanager.models.tax import UserProfile
from itemmanager.forms import TaxCalculationForm
from decimal import Decimal

def calculate_tax(request):
    if request.method == 'POST':
        form = TaxCalculationForm(request.POST)

        if form.is_valid():
            try:
                income = Decimal(form.cleaned_data['income'])
                deductions = Decimal(form.cleaned_data['deductions'] or 0)
                exemptions = Decimal(form.cleaned_data['exemptions'] or 0)

                taxable_income = income - deductions - exemptions

                if taxable_income <= 250000:
                    tax_rate = Decimal('0.0')
                elif taxable_income <= 500000:
                    tax_rate = Decimal('0.05')
                elif taxable_income <= 1000000:
                    tax_rate = Decimal('0.2')
                else:
                    tax_rate = Decimal('0.3')

                tax_percentage = tax_rate * 100  # To display as a percentage

                tax_liability = taxable_income * tax_rate

                # Format Decimal values for database storage
                income = income.quantize(Decimal("0.00"))
                deductions = deductions.quantize(Decimal("0.00"))
                exemptions = exemptions.quantize(Decimal("0.00"))
                tax_liability = tax_liability.quantize(Decimal("0.00"))
                tax_percentage = tax_percentage.quantize(Decimal("0.00"))

                user_profile = UserProfile(
                    annual_income=income,
                    deductions=deductions,
                    exemptions=exemptions,
                    tax_liability=tax_liability,
                    tax_percentage=tax_percentage,
                )
                user_profile.save()

                return render(request, 'tax_calculation/tax_result.html', {'user_profile': user_profile})
            except Exception as e:
                # Handle any potential errors related to extremely large numbers here
                error_message = str(e)
                return render(request, 'tax_calculation/tax_form.html', {'form': form, 'error_message': error_message})

    else:
        form = TaxCalculationForm()

    return render(request, 'tax_calculation/tax_form.html', {'form': form})
