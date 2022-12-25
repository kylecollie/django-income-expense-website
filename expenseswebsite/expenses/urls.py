from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="expenses"),
    path('add-expense', views.add_expense, name="add-expenses"),
    path('edit-expense/<int:id>', views.expense_edit, name="edit-expense"),
    path('expense-delete/<int:id>', views.expense_delete, name="expense-delete"),
]