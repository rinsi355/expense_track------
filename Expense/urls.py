from django.urls import path
from . import views
urlpatterns = [
    path('dashboard/',views.dashboard,name='expense_dashboard'),
    path('add/',views.add_expense,name='add_expense'),
    path('list/',views.expense_list,name='expense_list'), 
    path('edit/<int:id>/',views.edit_expense,name='edit_expense'),
    path('delete/<int:id>/',views.delete_expense,name='delete_expense'),
    
]
