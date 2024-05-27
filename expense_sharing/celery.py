from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

from expense_sharing import settings
from expenses.tasks import send_weekly_summary

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "expense_sharing.settings")

app = Celery("expense_sharing")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=7, minute=0, day_of_week="sunday"),
        send_weekly_summary.s(),
    )
