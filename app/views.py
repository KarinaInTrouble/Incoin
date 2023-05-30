from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView
from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.db.models import Sum, Min, Max
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request,"index.html")

def signup(request):
    return render(request,"registration/signup.html")

@login_required 
def cabinet(request):
    return render(request,"cabinet.html")

@login_required 
def projects(request):
    query = Project.objects.filter(user=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
    else:
        form = ProjectForm()
    return render(request, 'projects.html', {'form': form, 'query': query})

@login_required 
def delete_project(request, id):
    project = Project.objects.get(id=id)
    if project.user == request.user:
        project.delete()
    return redirect('projects')
    

class AddCategoryCreate(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'categories.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = Category.objects.filter(user=self.request.user)
        return context

    def get_success_url(self):
        referer = self.request.META.get('HTTP_REFERER')
        if referer:
            return referer
@login_required 
def delete_category(request, id):
    category = Category.objects.get(id=id)
    if category.user == request.user:
        category.delete()
    return redirect('categories')

@login_required 
def income(request):
    query = Income.objects.filter(user=request.user)
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
    else:
        form = IncomeForm()
    income_sum = Income.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum']
    income_min = Income.objects.filter(user=request.user).aggregate(Min('amount'))['amount__min']
    income_max = Income.objects.filter(user=request.user).aggregate(Max('amount'))['amount__max']
    return render(request, 'income.html', {'income_sum': income_sum, 'income_min': income_min, 'income_max': income_max, 'query': query, 'form': form})
@login_required 
def expense(request):
    query = Expense.objects.filter(user=request.user)
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
    else:
        form = ExpenseForm()
    ex_sum = Expense.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum']
    ex_min = Expense.objects.filter(user=request.user).aggregate(Min('amount'))['amount__min']
    ex_max = Expense.objects.filter(user=request.user).aggregate(Max('amount'))['amount__max']
    return render(request, 'expense.html', {'ex_sum': ex_sum, 'ex_min': ex_min, 'ex_max': ex_max, 'query': query, 'form': form})

@login_required 
def task(request):
    return render(request,"task.html")

@login_required 
def dashboard(request):
    project_data = Income.objects.values('project__name').annotate(total_amount=Sum('amount'))
    category_data = Income.objects.values('category__name').annotate(total_amount=Sum('amount'))
    date_data = Income.objects.values('date').annotate(total_amount=Sum('amount'))

    # Convert Decimal values to float before serializing
    project_data = [
        {'project__name': item['project__name'], 'total_amount': float(item['total_amount'])}
        for item in project_data
    ]
    category_data = [
        {'category__name': item['category__name'], 'total_amount': float(item['total_amount'])}
        for item in category_data
    ]
    date_data = [
        {'date': item['date'], 'total_amount': float(item['total_amount'])}
        for item in date_data
    ]

    project_d = Expense.objects.values('project__name').annotate(total_amount=Sum('amount'))
    category_d = Expense.objects.values('category__name').annotate(total_amount=Sum('amount'))
    date_d = Expense.objects.values('date').annotate(total_amount=Sum('amount'))

    # Convert Decimal values to float before serializing
    project_d = [
        {'project__name': item['project__name'], 'total_amount': float(item['total_amount'])}
        for item in project_d
    ]
    category_d = [
        {'category__name': item['category__name'], 'total_amount': float(item['total_amount'])}
        for item in category_d
    ]
    date_d = [
        {'date': item['date'], 'total_amount': float(item['total_amount'])}
        for item in date_d
    ]

    income_data = Income.objects.filter(user=request.user).aggregate(total_amount=Sum('amount'))
    expense_data = Expense.objects.filter(user=request.user).aggregate(total_amount=Sum('amount'))

    return render(request, 'dashboard.html', {
        'project_data': json.dumps(project_data, cls=DjangoJSONEncoder),
        'category_data': json.dumps(category_data, cls=DjangoJSONEncoder),
        'date_data': json.dumps(date_data, cls=DjangoJSONEncoder),
        'income_data': income_data,
        'expense_data': expense_data,
        'project_d': json.dumps(project_d, cls=DjangoJSONEncoder),
        'category_d': json.dumps(category_d, cls=DjangoJSONEncoder),
        'date_d': json.dumps(date_d, cls=DjangoJSONEncoder),
    })

"""
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'create_project.html', {'form': form})

def delete_project(request, pk):
    project = Project.objects.get(pk=pk)
    project.delete()
    return redirect('project_list')

def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'create_category.html', {'form': form})

def delete_category(request, pk):
    category = Category.objects.get(pk=pk)
    category.delete()
    return redirect('category_list')

def create_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            return redirect('income_list')
    else:
        form = IncomeForm()
    return render(request, 'create_income.html', {'form': form})

def delete_income(request, pk):
    income = Income.objects.get(pk=pk)
    income.delete()
    return redirect('income_list')

def create_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'create_expense.html', {'form': form})

def delete_expense(request, pk):
    expense = Expense.objects.get(pk=pk)
    expense.delete()
    return redirect('expense_list')

def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'create_task.html', {'form': form})

def delete_task(request, pk):
    task = Task.objects.get(pk=pk)
    task.delete()
    return redirect('task_list')

def edit_task(request, pk):
    task = Task.objects.get(pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect
"""

from django.shortcuts import render
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from .models import Income, Expense, Category, Project
from django.db.models import Avg, Max, Min, Sum
from io import BytesIO

@login_required 
def generate_report(request):
    # Get the data to be displayed in the report

    # Incomes
    average_income = Income.objects.aggregate(Avg('amount'))['amount__avg']
    max_income = Income.objects.aggregate(Max('amount'))['amount__max']
    min_income = Income.objects.aggregate(Min('amount'))['amount__min']
    total_income = Income.objects.aggregate(Sum('amount'))['amount__sum']

    # Expenses
    average_expense = Expense.objects.aggregate(Avg('amount'))['amount__avg']
    max_expense = Expense.objects.aggregate(Max('amount'))['amount__max']
    min_expense = Expense.objects.aggregate(Min('amount'))['amount__min']
    total_expense = Expense.objects.aggregate(Sum('amount'))['amount__sum']

    profit = total_income - total_expense

    category_max_income = Category.objects.filter(income__amount=max_income).first()
    category_min_income = Category.objects.filter(income__amount=min_income).first()
    project_max_income = Project.objects.filter(income__amount=max_income).first()
    project_min_income = Project.objects.filter(income__amount=min_income).first()

    month_max_income = Income.objects.values('date__year', 'date__month').annotate(total=Sum('amount')).order_by('-total').first()
    month_max_expense = Expense.objects.values('date__year', 'date__month').annotate(total=Sum('amount')).order_by('-total').first()
    month_min_income = Income.objects.values('date__year', 'date__month').annotate(total=Sum('amount')).order_by('total').first()
    month_min_expense = Expense.objects.values('date__year', 'date__month').annotate(total=Sum('amount')).order_by('total').first()

    income_table_data = Income.objects.values('amount', 'category__name', 'project__name', 'date')
    expense_table_data = Expense.objects.values('amount', 'category__name', 'project__name', 'date')

    # Load the PDF template
    template = get_template('report.html')

    # Fill the template context with data
    context = {
        'average_income': average_income,
        'max_income': max_income,
        'min_income': min_income,
        'average_expense': average_expense,
        'max_expense': max_expense,
        'min_expense': min_expense,
        'profit': profit,
        'category_max_income': category_max_income,
        'category_min_income': category_min_income,
        'project_max_income': project_max_income,
        'project_min_income': project_min_income,
        'month_max_income': month_max_income,
        'month_max_expense': month_max_expense,
        'month_min_income': month_min_income,
        'month_min_expense': month_min_expense,
        'income_table_data': income_table_data,
        'expense_table_data': expense_table_data,
        'total_income': total_income,
        'total_expense': total_expense,
    }

    html = template.render(context)

    # Create a file-like buffer to receive PDF data
    buffer = BytesIO()

    # Convert HTML to PDF with proper encoding and font configuration
    pisa_status = pisa.CreatePDF(
        html.encode('UTF-8'),
        dest=buffer,
        encoding='UTF-8'
    )

    # If PDF generation was successful, return the PDF as response
    if pisa_status.err:
        return HttpResponse('Error creating PDF report', status=500)
    
    # Set the buffer's file pointer at the beginning of the buffer
    buffer.seek(0)

    # Create an HttpResponse object with PDF content
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    response['Content-Encoding'] = 'UTF-8'

    return response
