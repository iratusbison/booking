
from django.shortcuts import render, redirect, get_object_or_404
from itemmanager.models.expense import Expense, ESection
from itemmanager.forms import ExpenseForm, ESectionForm
from django.db.models import Sum
from decimal import Decimal
from itemmanager.views.view_income import calculate_total_income_pool

def esection_list(request):
    esections = ESection.objects.all()
    total_expenses = Expense.objects.aggregate(total=Sum('amount'))['total']
    total_expenses = total_expenses or Decimal('0')  # Convert to Decimal

    # Convert to float for session storage
    total_expenses_float = float(total_expenses)

    total_income_pool = calculate_total_income_pool()

    # Subtract the total expenses from the total income pool
    total_income_pool -= total_expenses

    # Store the value in the session
    request.session['total_expenses'] = total_expenses_float
    request.session['total_income_pool'] = str(total_income_pool)

    if request.method == 'POST' and 'delete_esection' in request.POST:
        esection_id = request.POST['delete_esection']
        esection = ESection.objects.get(pk=esection_id)
        esection.delete()
        return redirect('esection_list')


    return render(request, 'esection_list.html', {'esections': esections, 'total_expenses': total_expenses, 'total_income_pool' : total_income_pool})

def add_esection(request):
    if request.method == 'POST':
        form = ESectionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('esection_list')
    else:
        form = ESectionForm()

    return render(request, 'add_esection.html', {'form': form})



from decimal import Decimal

def expense_list(request, esection_id):
    esection = get_object_or_404(ESection, pk=esection_id)
    expenses = Expense.objects.filter(esection=esection)
    esection = ESection.objects.get(pk=esection_id)

    # Check if total_expenses is None and handle it
    total_expenses = expenses.aggregate(total=Sum('amount'))['total']
    total_expenses_float = Decimal(total_expenses) if total_expenses is not None else Decimal('0')
    total_income_pool = Decimal(request.session.get('total_income_pool', 0))
    return render(request, 'expense_list.html', {'expenses': expenses, 'total_expenses': total_expenses_float, 'esection': esection, 'total_income_pool': total_income_pool})



from decimal import Decimal

# ...

def add_expense(request, esection_id):
    esection = ESection.objects.get(pk=esection_id)

    # Retrieve the current total_income_pool from the session, converting it back to Decimal
    total_income_pool = Decimal(request.session.get('total_income_pool', 0))

    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.instance.esection = esection
            form.save()

            # Deduct the expense amount from the total_income_pool
            expense_amount = form.cleaned_data['amount']
            total_income_pool -= Decimal(expense_amount)

            # Update the session with the new total_income_pool value, converted to string
            request.session['total_income_pool'] = str(total_income_pool)

            return redirect('expense_list', esection_id=esection_id)
    else:
        form = ExpenseForm()

    expenses = Expense.objects.filter(esection=esection)
    total_expense = sum(expense.amount for expense in expenses)

    return render(request, 'add_expense.html', {'esection': esection, 'form': form, 'expenses': expenses, 'total_expense': total_expense, 'total_income_pool': total_income_pool})



def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, pk=expense_id)
    esection_id = expense.esection.id
    if request.method == 'POST':
        expense.delete()
        return redirect('expense_list',esection_id=esection_id)
    return render(request, 'delete_expense.html', {'expense': expense, 'esection_id':esection_id})



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


def generate_pdf(request, esection_id):
    esection = get_object_or_404(ESection, pk=esection_id)
    expenses = Expense.objects.filter(esection=esection)

    # Calculate the total expense
    total_expense = sum(expense.amount for expense in expenses)

    # Create an in-memory PDF file
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    # Add a line with the total expense
    styles = getSampleStyleSheet()
    total_expense_text = Paragraph(f'<b>Total Expense:</b> Rs {total_expense}', styles['Normal'])
    elements.append(total_expense_text)

    # Create a data list for the table
    data = [["Date", "Description", "Amount"]]  # Header row
    for expense in expenses:
        data.append([expense.date, expense.description, f'Rs {expense.amount}'])

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
    response['Content-Disposition'] = f'attachment; filename="expense_list_{esection_id}.pdf"'

    # Close the buffer
    buffer.close()

    return response
