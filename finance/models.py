from django.db import models
from django.contrib.auth.models import User

class Transaction(models.Model):
    EXPENSE = 'expense'
    INCOME = 'income'
    TYPE_CHOICES = [(EXPENSE, 'Expense'), (INCOME, 'Income')]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.user} | {self.date} | {self.category} | {self.amount}"