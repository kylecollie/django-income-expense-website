import json
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Source, UserIncome
from userpreferences.models import UserPreference
from django.http import JsonResponse

# Create your views here.

def search_income(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        income = UserIncome.objects.filter(
            amount__istartswith = search_str, owner = request.user) | UserIncome.objects.filter(
                date__istartswith = search_str, owner = request.user) | UserIncome.objects.filter(
                    description__icontains = search_str, owner = request.user) | UserIncome.objects.filter(
                        source__istartswith = search_str, owner = request.user)

        data = income.values()

        return JsonResponse(list(data), safe=False)

@login_required(login_url='/authentication/login')
def index(request):
    sources = Source.objects.all()
    income = UserIncome.objects.filter(owner=request.user)
    paginator = Paginator(income, 2)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency = UserPreference.objects.get(user=request.user).currency
    context = {
        'income': income,
        'page_obj': page_obj,
        'currency': currency,
    }
    return render(request, 'income/index.html', context)


def add_income(request):
    sources = Source.objects.all()
    context = {
        'sources': sources,
        'values': request.POST
    }
    if request.method =='GET':
        return render(request, 'income/add_income.html', context)
        

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['date']
        source = request.POST['source']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/add_income.html', context)

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'income/add_income.html', context)
        
        UserIncome.objects.create(owner=request.user, amount=amount, date=date, source=source, description=description)
        messages.success(request, 'Record saved succesfully')

        return redirect('income')

def income_edit(request, id):
    sources = Source.objects.all()
    income = UserIncome.objects.get(pk = id)
    context ={
        'sources': sources,
        'income': income,
        'values': income,
    }
    if request.method == 'GET':
        return render(request, 'income/edit-income.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['date']
        source = request.POST['source']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'incomes/edit_income.html', context)

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'income/edit_income.html', context)
        
        income.owner=request.user
        income.amount=amount
        income.date=date
        income.source=source
        income.description=description

        income.save()

        messages.success(request, 'Income updated succesfully')

        return redirect('income')

def income_delete(request, id):
    income = UserIncome.objects.get(pk = id)
    income.delete()
    messages.success(request, 'Income removed')
    return redirect('income')        