# expenses/models.py
from django.db import models


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)


class Expense(models.Model):
    EXPENSE_TYPE_CHOICES = [
        ("EQUAL", "Equal"),
        ("EXACT", "Exact"),
        ("PERCENT", "Percent"),
    ]
    expense_id = models.AutoField(primary_key=True)
    paid_by = models.ForeignKey(
        User, related_name="expenses_paid", on_delete=models.CASCADE
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    expense_type = models.CharField(max_length=10, choices=EXPENSE_TYPE_CHOICES)
    participants = models.ManyToManyField(User, related_name="expenses_participated")
    date_created = models.DateTimeField(auto_now_add=True)
    exact_amounts = models.JSONField(default=dict)
    percentages = models.JSONField(default=dict)


class Balance(models.Model):
    user_from = models.ForeignKey(
        User, related_name="balances_owed", on_delete=models.CASCADE
    )
    user_to = models.ForeignKey(
        User, related_name="balances_due", on_delete=models.CASCADE
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)


class ExactAmount(models.Model):
    expense = models.ForeignKey(
        Expense, related_name="exactamount_set", on_delete=models.CASCADE
    )
    participant = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)


class PercentageShare(models.Model):
    expense = models.ForeignKey(
        Expense, related_name="percentageshare_set", on_delete=models.CASCADE
    )
    participant = models.ForeignKey(User, on_delete=models.CASCADE)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
