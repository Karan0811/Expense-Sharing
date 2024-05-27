from django.contrib import admin
from .models import User, Balance, Expense, ExactAmount, PercentageShare
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from datetime import timedelta
from django.utils import timezone
import json

admin.site.register(User)
admin.site.register(Balance)
admin.site.register(Expense)
admin.site.register(ExactAmount)
admin.site.register(PercentageShare)

schedule, created = CrontabSchedule.objects.get_or_create(
    minute="0",
    hour="0",
    day_of_week="monday",
    day_of_month="*",
    month_of_year="*",
)

# Check if the PeriodicTask with the given name already exists
if not PeriodicTask.objects.filter(name="Send weekly summary").exists():
    PeriodicTask.objects.create(
        crontab=schedule,
        name="Send weekly summary",
        task="expenses.tasks.send_weekly_summary",
        start_time=timezone.now() + timedelta(seconds=30),
    )
else:
    print("Periodic task 'Send weekly summary' already exists.")
