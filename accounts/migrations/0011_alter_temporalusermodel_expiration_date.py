# Generated by Django 5.0.6 on 2024-06-19 00:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_alter_temporalusermodel_expiration_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temporalusermodel',
            name='expiration_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 20, 0, 3, 50, 514399, tzinfo=datetime.timezone.utc)),
        ),
    ]
