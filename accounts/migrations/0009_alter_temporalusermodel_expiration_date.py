# Generated by Django 5.0.6 on 2024-06-18 12:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_temporalusermodel_expiration_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temporalusermodel',
            name='expiration_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 19, 12, 37, 51, 467653, tzinfo=datetime.timezone.utc)),
        ),
    ]
