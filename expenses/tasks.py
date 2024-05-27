from celery import shared_task
from django.core.mail import send_mail
from django.apps import apps


@shared_task
def send_expense_email(expense_id):
    Expense = apps.get_model("expenses", "Expense")
    ExactAmount = apps.get_model("expenses", "ExactAmount")
    PercentageShare = apps.get_model("expenses", "PercentageShare")

    expense = Expense.objects.get(id=expense_id)
    for participant in expense.participants.all():
        amount_owed = 0
        if expense.expense_type == "EQUAL":
            amount_owed = round(expense.amount / expense.participants.count(), 2)
        elif expense.expense_type == "EXACT":
            exact_amount = ExactAmount.objects.get(
                expense=expense, participant=participant
            )
            amount_owed = exact_amount.amount
        elif expense.expense_type == "PERCENTAGE":
            percentage_share = PercentageShare.objects.get(
                expense=expense, participant=participant
            )
            amount_owed = round(expense.amount * (percentage_share.percentage / 100), 2)

        send_mail(
            "New Expense Added",
            f"You have been added to a new expense. You owe {amount_owed} for this expense.",
            "karanpamnani8@gmail.com",
            [participant.email],
            fail_silently=False,
        )


@shared_task
def send_weekly_summary():
    User = apps.get_model("expenses", "User")
    Balance = apps.get_model("expenses", "Balance")

    users = User.objects.all()
    for user in users:
        balances_from = Balance.objects.filter(user_from=user)
        balances_to = Balance.objects.filter(user_to=user)
        summary_from = "\n".join(
            [
                f"You owe {balance.amount} to {balance.user_to.name}"
                for balance in balances_from
            ]
        )
        summary_to = "\n".join(
            [
                f"{balance.user_from.name} owes you {balance.amount}"
                for balance in balances_to
            ]
        )

        summary = "Summary of your expenses:\n\n"
        if summary_from:
            summary += f"Amounts you owe:\n{summary_from}\n\n"
        if summary_to:
            summary += f"Amounts owed to you:\n{summary_to}\n\n"

        if summary_from or summary_to:
            send_mail(
                "Weekly Summary",
                summary,
                "karanpamnani8@gmail.com",
                [user.email],
                fail_silently=False,
            )
