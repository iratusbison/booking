from django.shortcuts import render

def total_view(request):
    # Retrieve the value from the session

    total_invest_amount_of_all_isections = request.session.get('total_invest_amount_of_all_isections',0)
    total_expenses = request.session.get('total_expenses',0)
    total_income = request.session.get('total_income',0)
    context = {
         'total_invest_amount_of_all_isections' : total_invest_amount_of_all_isections , 'total_expenses':total_expenses , 'total_income' : total_income}

    return render(request, 'total_template.html', context)
