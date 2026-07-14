from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from.models import Expense
from.forms import ExpenseForm
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Sum
from io import BytesIO
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from django.db.models.functions import TruncMonth
import json



@login_required

def add_expense(request):

    if request.method == 'POST':

        form = ExpenseForm(request.POST)

        if form.is_valid():

            expense = form.save(commit=False)

            expense.user = request.user

            expense.save()

            return redirect('expense_dashboard')

    else:

        form = ExpenseForm()

    return render(request, 'expense/add_expense.html', {'form': form})

def expense_list(request):
    expenses=Expense.objects.filter(user=request.user)
    search=request.GET.get('search')
    category=request.GET.get('category')
    date=request.GET.get('date')
    month=request.GET.get('month')
    

    if search:
        expenses=expenses.filter(category__icontains=search)
    if category:
        expenses=expenses.filter(category__icontains=category)
    if date:
        expenses=expenses.filter(date=date)
    if month and "-" in month:
        year,month_num=month.split("-")
        expenses=expenses.filter(
            date__year=int(year),
            date__month=int(month_num)
         )
    
    total = expenses.aggregate(total=Sum("amount"))
    monthly_total = expenses.aggregate(total=Sum('amount'))['total'] or 0

    return render(request, 'expense/expense_list.html',{'expenses':expenses, 'monthly_total':monthly_total})
def edit_expense(request, id):

    expense = get_object_or_404(Expense, id=id, user=request.user)

    if request.method == 'POST':

        form = ExpenseForm(request.POST, instance=expense)

        if form.is_valid():

            form.save()

            return redirect('expense_list')

    else:

        form = ExpenseForm(instance=expense)

    return render(request, 'expense/edit_expense.html', {'form': form})
def delete_expense(request,id):
    expense =get_object_or_404(Expense,id=id,user=request.user)
    expense.delete()
    return redirect('expense_list')

def dashboard(request):

    total_expense = 0
    total_records = 0
    recent_expenses = []
    chart =  None
    months = []
    amounts=[]

    expenses = Expense.objects.filter(user=request.user)
    category_data = expenses.values("category").annotate(

    total=Sum("amount")

    )

    chart = ""

    if category_data.exists():
       
       labels = []
       values = []

       for item in category_data:
           
           labels.append(item["category"])
           values.append(float(item["total"]))
       
       plt.figure(figsize=(5,5))

       plt.pie(

           values,

           labels=labels,

           autopct="%1.1f%%",

           startangle=90

        )
       plt.title("Expenses by Category")

       buffer = BytesIO()

       plt.savefig(buffer, format="png")

       buffer.seek(0)

       chart = base64.b64encode(buffer.getvalue()).decode()

       buffer.close()

       plt.close()

       total_expense=expenses.aggregate(total=Sum('amount'))['total'] or 0

       total_records = expenses.count()

       recent_expenses=expenses.order_by('-id')[:5]

       monthly_data = expenses.annotate(

               month=TruncMonth('date')

       ).values('month').annotate(

             total=Sum('amount')

       ).order_by('month')

       months = []

       amounts = []

       for item in monthly_data:

            months.append(item['month'].strftime('%b'))

            amounts.append(float(item['total']))

    context = {

            'total_expense': total_expense,

             'total_records': total_records,
        
             'recent_expenses':recent_expenses,

             'chart':chart,

             'months': json.dumps(months),

             'amounts': json.dumps(amounts),

    }
    return render(request, 'expense/dashboard.html',context)