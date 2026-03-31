from django import forms

from .models import Transaction

class TransactionForm(forms.ModelForm):
    EXPENSE = 'expense'
    INCOME = 'income'
    TYPE_CHOICES = [(EXPENSE, 'Expense'), (INCOME, 'Income')]

    date = forms.DateField()
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    category = forms.CharField(max_length=100)
    description = forms.CharField(max_length=255, required=False)
    
    type = forms.CharField(
        max_length=10,
        widget=forms.Select(choices=TYPE_CHOICES),
    )
    created_at = forms.DateTimeField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Transaction
        fields = ['date', 'amount', 'category', 'description', 'type']