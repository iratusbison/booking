from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views, get_user
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import TSUser


def index(request):
    return render(request, 'core/index.html')

def login(request):
    if request.POST:
        auth_logout(request)
        username = password = ''
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            tsuser = TSUser.objects.get_user(user=user)
            request.session['ts_user'] = {}
            request.session['ts_user']['major'] = tsuser.major_string()
            request.session['ts_user']['role'] = tsuser.role_string()
            request.session['ts_user']['major_short'] = tsuser.major
            request.session['ts_user']['role_short'] = tsuser.role
            request.session['ts_user']['is_admin'] = tsuser.is_admin()

            auth_login(request, user)
            return redirect('/dashboard/')
        else:
            return render(request, 'core/login.html', {'error': True})
    else:
        if request.user.is_authenticated:
            return redirect('/dashboard/')
        return render(request, 'core/login.html')

def logout(request):
    auth_logout(request)
    return redirect('/')


@login_required(login_url='/login')
def dashboard(request):

    total_invest_amount_of_all_isections = request.session.get('total_invest_amount_of_all_isections',0)
    total_income_pool = request.session.get('total_income_pool',0)
    total_expenses = request.session.get('total_expenses',0)
    total_income = request.session.get('total_income',0)
    total_monthly_income = request.session.get('total_monthly_income',0)
    context = {
         'total_expenses':total_expenses , 'total_income' : total_income ,'total_income_pool':total_income_pool, 'total_invest_amount_of_all_isections' : total_invest_amount_of_all_isections, 'total_monthly_income' : total_monthly_income}

    return render(request, 'core/dashboard.html', context)

@login_required(login_url='/login')
def profile(request):
    # TODO create profile template
    return render(request, 'core/dashboard.html')

def print(request):
    return render(request, 'core/construction.html', {'active_tab': 'print'})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from .models import Subscription
from datetime import date, timedelta


@login_required
def subscribe(request):
    user = request.user
    try:
        subscription = Subscription.objects.get(user=user)
        # Check if the subscription is active
        if subscription.subscription_end_date >= date.today():
            return redirect('home')
    except Subscription.DoesNotExist:
        pass

    # Handle the subscription payment here (e.g., integrate with a payment gateway)
    # After successful payment, set the subscription dates
    subscription_start_date = date.today()
    subscription_end_date = subscription_start_date + timedelta(days=365)  # 1 year subscription
    Subscription.objects.create(user=user, subscription_start_date=subscription_start_date, subscription_end_date=subscription_end_date)

    return redirect('home')

@method_decorator(login_required, name='dispatch')
class HomeView(View):
    def get(self, request):
        user = request.user
        try:
            subscription = Subscription.objects.get(user=user)
            # Check if the subscription is active

            if subscription.subscription_end_date >= date.today():
                return render(request, 'core/home.html', {'subscription': subscription})
        except Subscription.DoesNotExist:
            pass

        # If no active subscription, display a message
        return render(request, 'core/home.html', {'message': 'Your subscription has expired. Please renew it.'})
