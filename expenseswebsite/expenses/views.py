from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from userpreferences.models import UserPreference
from django.core.paginator import Paginator
import json
from django.http import JsonResponse

# Create your views here.

def search_expenses(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        expenses = Expense.objects.filter(
            amount__istartswith = search_str, owner = request.user) | Expense.objects.filter(
                date__istartswith = search_str, owner = request.user) | Expense.objects.filter(
                    description__icontains = search_str, owner = request.user) | Expense.objects.filter(
                        category__istartswith = search_str, owner = request.user)

        data = expenses.values()

        return JsonResponse(list(data), safe=False)


@login_required(login_url='/authentication/login')
def index(request):
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 2)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency = UserPreference.objects.get(user=request.user).currency
    context = {
        'expenses': expenses,
        'page_obj': page_obj,
        'currency': currency,
    }
    return render(request, 'expenses/index.html', context)


def add_expense(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values': request.POST
    }
    if request.method =='GET':
        return render(request, 'expenses/add_expense.html', context)
        

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['date']
        category = request.POST['category']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/add_expense.html', context)

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'expenses/add_expense.html', context)
        
        Expense.objects.create(owner=request.user, amount=amount, date=date, category=category, description=description)
        messages.success(request, 'Expense saved succesfully')

        return redirect('expenses')

def expense_edit(request, id):
    categories = Category.objects.all()
    expense = Expense.objects.get(pk = id)
    context ={
        'categories': categories,
        'expense': expense,
        'values': expense,
    }
    if request.method == 'GET':
        return render(request, 'expenses/edit-expense.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['date']
        category = request.POST['category']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/edit_expense.html', context)

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'expenses/edit_expense.html', context)
        
        expense.owner=request.user
        expense.amount=amount
        expense.date=date
        expense.category=category
        expense.description=description

        expense.save()

        messages.success(request, 'Expense updated succesfully')

        return redirect('expenses')

def expense_delete(request, id):
    expense = Expense.objects.get(pk = id)
    expense.delete()
    messages.success(request, 'Expense removed')
    return redirect('expenses')