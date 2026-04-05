from django.shortcuts import render, redirect
import pandas as pd
import plotly.express as px
from plotly.offline import plot

from .models import Transaction
from .forms import TransactionForm

# class CSVUploadView(APIView):
#     parser_classes = [MultiPartParser]

#     def post(self, request):
#         file = request.FILES.get('file')
#         if not file:
#             return Response({'error': 'No file provided'}, status=400)

#         try:
#             df = pd.read_csv(file)

#             # normalize column names (lowercase, strip spaces)
#             df.columns = df.columns.str.lower().str.strip()

#             # expect columns: date, amount, category, description, type
#             required = {'date', 'amount', 'category', 'type'}
#             if not required.issubset(df.columns):
#                 return Response({'error': f'CSV must contain columns: {required}'}, status=400)

#             # clean the data
#             df['date'] = pd.to_datetime(df['date'], errors='coerce')
#             df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
#             df = df.dropna(subset=['date', 'amount'])
#             df['description'] = df.get('description', '').fillna('')
#             df['category'] = df['category'].str.strip().str.title()
#             df['type'] = df['type'].str.lower().str.strip()
#             df = df[df['type'].isin(['income', 'expense'])]

#             # bulk create
#             transactions = [
#                 Transaction(
#                     user=request.user,
#                     date=row['date'].date(),
#                     amount=row['amount'],
#                     category=row['category'],
#                     description=row['description'],
#                     type=row['type'],
#                 )
#                 for _, row in df.iterrows()
#             ]
#             Transaction.objects.bulk_create(transactions)

#             return Response({'created': len(transactions)}, status=201)

#         except Exception as e:
#             return Response({'error': str(e)}, status=400)


# class DashboardView(APIView):

#     def get(self, request):
#         qs = Transaction.objects.filter(user=request.user).values(
#             'date', 'amount', 'category', 'type'
#         )
#         if not qs.exists():
#             return Response({'message': 'No transactions found'})

#         df = pd.DataFrame(list(qs))
#         df['date'] = pd.to_datetime(df['date'])
#         df['month'] = df['date'].dt.to_period('M').astype(str)

#         # monthly income vs expenses
#         monthly = (
#             df.groupby(['month', 'type'])['amount']
#             .sum()
#             .unstack(fill_value=0)
#             .reset_index()
#             .rename(columns={'income': 'income', 'expense': 'expenses'})
#         )
#         monthly_data = monthly.to_dict(orient='records')

#         # spending by category (expenses only)
#         by_category = (
#             df[df['type'] == 'expense']
#             .groupby('category')['amount']
#             .sum()
#             .reset_index()
#             .sort_values('amount', ascending=False)
#             .to_dict(orient='records')
#         )

#         # summary stats
#         total_income = float(df[df['type'] == 'income']['amount'].sum())
#         total_expenses = float(df[df['type'] == 'expense']['amount'].sum())

#         return Response({
#             'summary': {
#                 'total_income': total_income,
#                 'total_expenses': total_expenses,
#                 'net': total_income - total_expenses,
#             },
#             'monthly_totals': monthly_data,
#             'by_category': by_category,
#         })
    


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


from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json
from pathlib import Path

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