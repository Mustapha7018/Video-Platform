# Generated by Django 5.0.6 on 2024-06-12 20:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_temporalusermodel_expiration_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temporalusermodel',
            name='expiration_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 13, 20, 40, 35, 452243, tzinfo=datetime.timezone.utc)),
        ),
    ]
