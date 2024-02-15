from django.shortcuts import render, redirect, get_object_or_404
from itemmanager.models.income import Income, IncSection, MonthlyIncome
from itemmanager.forms import IncomeForm, IncSectionForm, MonthlyIncomeForm
from django.db.models import Sum
from decimal import Decimal
from django.db.models import F, ExpressionWrapper, DecimalField
from django.db.models import Sum, Value


def apply_gst(income_amount):
    # Calculate GST of 18%
  '''
    gst_rate = Decimal('0.18')
    gst_amount = income_amount * gst_rate
    total_amount = income_amount + gst_amount

    return total_amount
    '''
  # Calculate the GST amount
  gst_amount = income_amount / (1 + Decimal('0.18')) * Decimal('0.18')
    # Calculate the net amount (amount without GST)
  net_amount = income_amount - gst_amount
  return net_amount, gst_amount



from django.contrib.auth.decorators import login_required
@login_required(login_url='/login')
def incsection_list(request):
    incsections = IncSection.objects.all()

    total_income = Income.objects.aggregate(total=Sum('amount'))['total']
    total_income = total_income or Decimal('0')  # Convert to Decimal

    # Apply GST
    #total_income_with_gst = apply_gst(total_income)

    # Convert to float for session storage
    total_income_float = float(total_income)

    # Store the value in the session
    request.session['total_income'] = total_income_float

    if request.method == 'POST' and 'delete_incsection' in request.POST:
        incsection_id = request.POST['delete_incsection']
        incsection = IncSection.objects.get(pk=incsection_id)
        incsection.delete()
        return redirect('incsection_list')

    return render(request, 'incsection_list.html', {'incsections': incsections, 'total_income': total_income})

@login_required(login_url='/login')
def add_incsection(request):
    if request.method == 'POST':
        form = IncSectionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('incsection_list')
    else:
        form = IncSectionForm()

    return render(request, 'add_incsection.html', {'form': form})

@login_required(login_url='/login')
def income_list(request, incsection_id):
    incsection = get_object_or_404(IncSection, pk=incsection_id)
    incomes = Income.objects.filter(incsection=incsection)

    # Apply GST to each income
    #for income in incomes:
       # income.amount_with_gst = apply_gst(income.amount)

    incsection = IncSection.objects.get(pk=incsection_id)
    total_income = incomes.aggregate(total=Sum('amount'))['total']

    if total_income is not None:
        # Apply GST to the total income
        total_income = (total_income)
    else:
        total_income = Decimal('0.00')

    return render(request, 'income_list.html', {'incomes': incomes, 'total_income': total_income, 'incsection': incsection})

@login_required(login_url='/login')
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
@login_required(login_url='/login')
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

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from io import BytesIO
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

def generate_pdf_income(request, incsection_id):
    incsection = get_object_or_404(IncSection, pk=incsection_id)
    incomes = Income.objects.filter(incsection=incsection)

    # Calculate the total income
    total_income = sum(income.amount for income in incomes)

    # Create an in-memory PDF file
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    # Add a line with the total expense
    styles = getSampleStyleSheet()
    total_income_text = Paragraph(f'<b>Total income:</b> Rs {total_income}', styles['Normal'])
    elements.append(total_income_text)

    # Create a data list for the table
    data = [["Date", "Description", "Amount"]]  # Header row
    for income in incomes:
        data.append([income.date, income.description, f'Rs {income.amount}'])

    # Define a custom table style
    custom_table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), (0.2, 0.2, 0.2)),
        ('TEXTCOLOR', (0, 0), (-1, 0), (1, 1, 1)),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), (0.9, 0.9, 0.9)),
        ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0))
    ])

    # Create the table with the custom style
    table = Table(data)
    table.setStyle(custom_table_style)

    # Add the table to the elements
    elements.append(table)

    # Build the PDF document
    doc.build(elements)

    # Reset the buffer's position to the start
    buffer.seek(0)

    # Create a Django HttpResponse with the PDF file
    response = HttpResponse(buffer.read(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="income_list_{incsection_id}.pdf"'

    # Close the buffer
    buffer.close()

    return response
@login_required(login_url='/login')
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
@login_required(login_url='/login')
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
@login_required(login_url='/login')
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

from django.shortcuts import render, get_object_or_404

@login_required(login_url='/login')
def income_detail(request, income_id):
    # Retrieve the income object or return a 404 error if not found
    income = get_object_or_404(Income, pk=income_id)

    gst_amount = income.amount - (income.amount/ (1 + Decimal('0.18')))
    net_price = income.amount - gst_amount

    rounded_gst_amount = round(gst_amount, 2)
    rounded_net_price = round(net_price, 2)

    total_amount = income.amount + income.other_charges

    # You can customize the details you want to display here
    income_details = {
        'Description': income.description,
        'Amount': income.amount,
        'other_charges' : income.other_charges,
        'gst_amount' : rounded_gst_amount,
        'net_price' : rounded_net_price,
        'Total Amount': total_amount,
        'Date': income.date,
        'Booked by': income.reserver,
        'Bride': income.bride,
        'Groom': income.groom,
        'Address': income.reserver_address,
        'Phone': income.reserver_phone,
        'Aadhar': income.reserver_aadhar,
        'Checkin Datetime': income.checkin_datetime,
        'Checkout Datetime': income.checkout_datetime,
        'Status': income.status,
        'Income Section': income.incsection.name if income.incsection else None
    }
    return render(request, 'income_detail.html', {'income_details': income_details, 'income_id': income_id})

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.units import inch
from django.http import HttpResponse
from django.template.loader import render_to_string
from io import BytesIO
from decimal import Decimal
from itemmanager.models.income import Income
from django.shortcuts import get_object_or_404


def generate_bill(data):
    # Create a buffer to hold the PDF data
    buffer = BytesIO()

    # Create a new PDF document
    doc = SimpleDocTemplate(buffer, pagesize=A4)

    # Define styles for the document
    styles = getSampleStyleSheet()

    # Create a list to hold the PDF elements
    elements = []
    '''
    # Add a title
    elements.append(Paragraph("SV Mahal / AKS Inn", styles["Title"]))

    elements.append(Paragraph("No.192/1A 1B, Vandavasi Road, Sevilimedu, Kanchipuram - 631502", styles["BodyText"]))
    elements.append(Paragraph("Phone: 9842254415, 9443733265, 9994195966", styles["BodyText"]))
    elements.append(Paragraph("Email: svmahalaksinn@gmail.com", styles["BodyText"]))
    elements.append(Paragraph("GST: 33ADDFS68571Z8", styles["BodyText"]))
    elements.append(Paragraph("Bill Statement", styles['Title']))
    '''
    # Increase font size for table
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 12),  # Increase font size
        ('TOPPADDING', (0, 0), (-1, -1), 8),  # Add padding to the cells
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ])

    # Add data to the bill table
    bill_data = [
        ["Total Amount", f"Rs {data['Total Amount']}"],
        ["Amount", f"Rs {data['Amount']}"],
        ["Other Charges", f"Rs {data['other_charges']}"],
        ["GST Amount", f"Rs {data['gst_amount']}"],
        ["Net Price", f"Rs {data['net_price']}"],
        ["Date", data['Date']],
        ["Booked by", data['Reserver']],
        ["Bride", data['Bride']],
        ["Groom", data['Groom']],
        ["Address", data['Reserver Address']],  # Handle newline characters here

        ["Phone", data['Reserver Phone']],
        ["Aadhar", data['Reserver Aadhar']],
        ["Checkin Datetime", data['Checkin Datetime']],
        ["Checkout Datetime", data['Checkout Datetime']],
    ]

    # Create the bill table
    bill_table = Table(bill_data, style=table_style)

    # Add the bill table to the elements
    elements.append(bill_table)

    # Build the PDF document
    doc.build(elements)

    # Reset the buffer's position to the start
    buffer.seek(0)

    return buffer


def generate_bill_view(request, income_id):
    # Retrieve the income object or return a 404 error if not found
    income = get_object_or_404(Income, pk=income_id)

    # Calculate the necessary attributes
    gst_amount = income.amount - (income.amount / (1 + Decimal('0.18')))
    net_price = income.amount - gst_amount
    total_amount = income.amount + income.other_charges


# Replace commas with newline characters for proper line breaks in the address
    address_with_line_breaks = income.reserver_address.replace(', ', '\n')
    # Populate data for the bill
    bill_data = {
        'Total Amount': total_amount,
        'Amount': income.amount,
        'other_charges': income.other_charges,
        'gst_amount': round(gst_amount, 2),
        'net_price': round(net_price, 2),
        'Date': income.date,
        'Reserver': income.reserver,
        'Bride': income.bride,
        'Groom': income.groom,
        'Reserver Address': address_with_line_breaks, # Pass the address as is

        'Reserver Phone': income.reserver_phone,
        'Reserver Aadhar': income.reserver_aadhar,
        'Checkin Datetime': income.checkin_datetime,
        'Checkout Datetime': income.checkout_datetime,
    }

    # Generate the bill PDF
    buffer = generate_bill(bill_data)

    # Create a Django HttpResponse with the PDF file
    response = HttpResponse(buffer.read(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="bill_statement_{income_id}.pdf"'

    # Close the buffer
    buffer.close()

    return response
