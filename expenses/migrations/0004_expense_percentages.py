# Generated by Django 4.1.5 on 2024-05-24 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("expenses", "0003_alter_expense_exact_amounts"),
    ]

    operations = [
        migrations.AddField(
            model_name="expense",
            name="percentages",
            field=models.JSONField(default=dict),
        ),
    ]
