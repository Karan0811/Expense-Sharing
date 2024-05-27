# expenses/views.py
from rest_framework import generics
from .models import User, Expense, Balance, ExactAmount, PercentageShare
from .serializers import (
    UserSerializer,
    ExpenseSerializer,
    BalanceSerializer,
    SimplifiedBalanceSerializer,
)
from .tasks import send_expense_email
from django.core.exceptions import ObjectDoesNotExist
from decimal import Decimal
from collections import defaultdict
from rest_framework import status
from rest_framework.response import Response


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ExpenseListCreateView(generics.ListCreateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    def perform_create(self, serializer):
        expense = serializer.save()
        self.split_expense(expense)
        # send_expense_email.delay(expense.expense_id)

    def split_expense(self, expense):
        if expense.expense_type == "EQUAL":
            self.split_equally()
        elif expense.expense_type == "EXACT":
            self.split_exactly(expense)
        elif expense.expense_type == "PERCENT":
            self.split_by_percentage(expense)

    def split_equally(self, expense):
        num_participants = expense.participants.count()
        share = round(expense.amount / num_participants, 2)
        remainder = expense.amount - (share * num_participants)

        for index, participant in enumerate(expense.participants.all()):
            final_share = share + (remainder if index == 0 else 0)
            self.update_balance(expense.paid_by, participant, final_share)

    def split_exactly(self, expense):
        total = sum(expense.exact_amounts.values())
        if total != expense.amount:
            raise ValueError("Total exact amounts do not match the expense amount")
        for user_id, amount in expense.exact_amounts.items():
            participant = User.objects.get(pk=user_id)
            ExactAmount.objects.create(
                expense=expense, participant=participant, amount=amount
            )
            self.update_balance(expense.paid_by, participant, Decimal(amount))

    def split_by_percentage(self, expense):
        total_percentage = sum(expense.percentages.values())
        if total_percentage != 100:
            raise ValueError("Total percentage does not sum to 100")
        for user_id, percentage in expense.percentages.items():
            participant = User.objects.get(pk=user_id)
            share = round(expense.amount * (Decimal(percentage) / 100), 2)
            PercentageShare.objects.create(
                expense=expense, participant=participant, percentage=percentage
            )
            self.update_balance(expense.paid_by, participant, share)

    def update_balance(self, payer, payee, amount):
        if payer == payee:
            return
        try:
            balance = Balance.objects.get(user_from=payer, user_to=payee)
        except ObjectDoesNotExist:
            balance = Balance.objects.create(user_from=payer, user_to=payee, amount=0)

        balance.amount += amount
        balance.save()


class BalanceListView(generics.ListAPIView):
    serializer_class = BalanceSerializer

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        return Balance.objects.filter(user_from_id=user_id).exclude(amount=0)


class SimplifiedBalanceListView(generics.ListAPIView):
    serializer_class = SimplifiedBalanceSerializer

    def get_queryset(self):
        balances = Balance.objects.all()
        user_balance_map = defaultdict(int)
        for balance in balances:
            user_balance_map[balance.user_from.name] -= balance.amount
            user_balance_map[balance.user_to.name] += balance.amount

        simplified_transactions = []
        creditors = [user for user, amount in user_balance_map.items() if amount > 0]
        debtors = [user for user, amount in user_balance_map.items() if amount < 0]
        while creditors and debtors:
            creditor = creditors.pop()
            debtor = debtors.pop()

            credit_amount = user_balance_map[creditor]
            debit_amount = -user_balance_map[debtor]

            min_amount = min(credit_amount, debit_amount)

            simplified_transactions.append(
                {
                    "user_from": debtor,
                    "user_to": creditor,
                    "amount": min_amount,
                }
            )
            user_balance_map[creditor] -= min_amount
            user_balance_map[debtor] += min_amount

            if user_balance_map[creditor] > 0:
                creditors.append(creditor)
            if user_balance_map[debtor] < 0:
                debtors.append(debtor)
        return simplified_transactions

    def list(self):
        queryset = self.get_queryset()
        return Response(queryset, status=status.HTTP_200_OK)
