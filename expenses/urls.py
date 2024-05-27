# expenses/urls.py
from django.urls import path
from .views import (
    UserListCreateView,
    ExpenseListCreateView,
    BalanceListView,
    SimplifiedBalanceListView,
)

urlpatterns = [
    path("users/", UserListCreateView.as_view(), name="user-list-create"),
    path("expenses/", ExpenseListCreateView.as_view(), name="expense-list-create"),
    path("balances/<int:user_id>/", BalanceListView.as_view(), name="balance-list"),
    path(
        "simplified-balances/",
        SimplifiedBalanceListView.as_view(),
        name="simplified-balance-list",
    ),
]
