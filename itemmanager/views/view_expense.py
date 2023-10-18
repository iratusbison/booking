
from django.shortcuts import render, redirect, get_object_or_404
from itemmanager.models.expense import Expense, ESection
from itemmanager.forms import ExpenseForm, ESectionForm
from django.db.models import Sum



def esection_list(request):
    esections = ESection.objects.all()
    total_expenses = Expense.objects.aggregate(total=Sum('amount'))['total']

    if request.method == 'POST' and 'delete_esection' in request.POST:
        esection_id = request.POST['delete_esection']
        esection = ESection.objects.get(pk=esection_id)
        esection.delete()
        return redirect('esection_list')

    return render(request, 'esection_list.html', {'esections': esections, 'total_expenses': total_expenses})

def add_esection(request):
    if request.method == 'POST':
        form = ESectionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('esection_list')
    else:
        form = ESectionForm()

    return render(request, 'add_esection.html', {'form': form})



def expense_list(request, esection_id):
    esection = get_object_or_404(ESection, pk=esection_id)
    expenses = Expense.objects.filter(esection=esection)
    esection = ESection.objects.get(pk=esection_id)
    total_expenses = expenses.aggregate(total=Sum('amount'))['total']
    return render(request, 'expense_list.html', {'expenses': expenses, 'total_expenses': total_expenses, 'esection':esection})

def add_expense(request,esection_id):
    esection = ESection.objects.get(pk=esection_id)
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.instance.esection = esection
            form.save()
            return redirect('expense_list',esection_id=esection_id)
    else:
        form = ExpenseForm()

    expenses = Expense.objects.filter(esection=esection)
    total_expense = sum(expense.amount for expense in expenses)

    return render(request, 'add_expense.html', {'esection': esection, 'form': form, 'expenses': expenses, 'total_expense': total_expense})


def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, pk=expense_id)
    esection_id = expense.esection.id
    if request.method == 'POST':
        expense.delete()
        return redirect('expense_list',esection_id=esection_id)
    return render(request, 'delete_expense.html', {'expense': expense, 'esection_id':esection_id})



from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from io import BytesIO

def generate_pdf(request, esection_id):
    esection = get_object_or_404(ESection, pk=esection_id)
    expenses = Expense.objects.filter(esection=esection)

    # Create an in-memory PDF file
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    # Create a data list for the table
    data = [["Expense Date", "Amount","description"]]  # Header row
    for expense in expenses:
        data.append([expense.date, expense.amount, expense.description])

    # Create a table and style
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

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

