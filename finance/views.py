from django.shortcuts import render, redirect
import plotly.express as px
from plotly.offline import plot
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json
from pathlib import Path
from django.views.decorators.http import require_http_methods
from django.db.models import Sum
from collections import defaultdict

from .models import Transaction
from .forms import TransactionForm


def index(request):

    return render(request, 'finance/index.html')

def transactions(request):
    transactions = Transaction.objects.filter(user=request.user).values('date', 'amount', 'category', 'description', 'type')

    amounts = [t['amount'] for t in transactions]
    categories = [t['category'] for t in transactions]
    types = [t['type'] for t in transactions]


    random_x = [100, 2000, 550]
    names = ['A', 'B', 'C']
    
    fig = px.pie(values=amounts, names=categories, title='Spending by Category')
    fig.update_layout(margin=dict(l=20, r=20, t=20, b=20), paper_bgcolor="LightSteelBlue")
    plot_div = plot(fig, output_type='div')


    context = {'transactions': transactions, 'plot': plot_div}
    return render(request, 'finance/transactions.html', context)

def add_transaction(request):

    if request.method != 'POST':
        # No data submitted; create a blank form.
        qs_transaction_types = Transaction.TYPE_CHOICES
        form = TransactionForm(initial={'type': qs_transaction_types})
    else:
        # POST data submitted; process data.
        form = TransactionForm(data=request.POST)
        if form.is_valid():
            new_transaction = form.save(commit=False)
            new_transaction.user = request.user
            new_transaction.save()
            
        return redirect('finance:transactions')
    
    # Display a blank or invalid form.
    context = {'form': form, 'transaction_types': qs_transaction_types,}
    return render(request, 'finance/add_transaction.html', context)


@login_required
def transactions_api(request):
    transactions = Transaction.objects.filter(user=request.user).values(
        'date', 'amount', 'category', 'description', 'type'
    )
    return JsonResponse(list(transactions), safe=False)

def get_vite_asset(filename):
    manifest_path = Path('staticfiles/frontend/.vite/manifest.json')
    with open(manifest_path) as f:
        manifest = json.load(f)
    return manifest[filename]['file']


@login_required
@require_http_methods(["POST"])
def add_transaction_api(request):
    data = json.loads(request.body)
    transaction = Transaction.objects.create(
        user=request.user,
        date=data['date'],
        amount=data['amount'],
        category=data['category'],
        description=data.get('description', ''),
        type=data['type'],
    )

    return JsonResponse({'status': 'ok', 'id': transaction.id})



@login_required
def finance_summary_api(request):
    transactions = Transaction.objects.filter(user=request.user)

    total_income = transactions.filter(type='income').aggregate(total=Sum('amount'))['total'] or 0
    total_expenses = transactions.filter(type='expense').aggregate(total=Sum('amount'))['total'] or 0

    by_category = transactions.filter(type='expense').values('category').annotate(total=Sum('amount')).order_by('-total')

    # Monthly totals
    monthly = defaultdict(lambda: {'income': 0, 'expense': 0})
    for t in transactions.values('date', 'amount', 'type'):
        month = t['date'].strftime('%Y-%m')
        monthly[month][t['type']] += float(t['amount'])

    monthly_data = [
        {'month': k, 'income': v['income'], 'expense': v['expense']}
        for k, v in sorted(monthly.items())
    ]

    return JsonResponse({
        'total_income': float(total_income),
        'total_expenses': float(total_expenses),
        'net': float(total_income) - float(total_expenses),
        'by_category': list(by_category),
        'monthly': monthly_data,
    })
