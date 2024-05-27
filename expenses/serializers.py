# expenses/serializers.py
from rest_framework import serializers
from .models import User, Expense, Balance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["user_id", "name", "email", "mobile"]


class ExpenseSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True
    )

    class Meta:
        model = Expense
        fields = [
            "expense_id",
            "paid_by",
            "amount",
            "expense_type",
            "participants",
            "date_created",
            "exact_amounts",
            "percentages",
        ]


class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balance
        fields = ["user_from", "user_to", "amount"]


class SimplifiedBalanceSerializer(serializers.Serializer):
    user_from = serializers.CharField()
    user_to = serializers.CharField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
